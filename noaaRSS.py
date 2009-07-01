import feedparser
import shelve
import re
import time
from model import *

class ThunderStorm(object):
    '''ThunderStorm class used to parse and store relevant information
    for a Severe ThunderStorm Alert'''
    def __init__(self, feedUrl, shelfPath, modelBind):
        #self.order=['location','effective','direction','expires','rain',
        #            'winds','lightining','hail']
        self.shelf = shelve.open(shelfPath, writeback=True)
        if "thunderstorm" not in self.shelf:
            self.shelf["thunderstorm"] = {}
        setupModel(modelBind)
        self.feedUrl = feedUrl
        #self.parse(feedparser.parse(feedUrl))

    def start(self):
        while True:
            print("Parsing feeds and handling notifies...")
            self.parse(feedparser.parse(self.feedUrl))
            time.sleep(600)

    def displayEntry(self, entry):
        id = entry['id'].split('=', 1)[1]
        state = id[0:2]
        sevLevel = entry['severity']
        effective = entry['effective']
        expires = entry['expires']
        urgency = entry['urgency']
        summary = entry['summary']

        print "\nID:            %s" % id
        print "State:         %s" % state
        print "Severity:      %s" % sevLevel
        print "Urgency:       %s" % urgency
        print "Effective:     %s" % effective
        print "Expires:       %s" % expires
        print "Summary:       %s" % summary
        print "Length of summary: %s\n" % len(summary)

    def parse(self, nfeed):
        ''' Itterate over the feed entries and store the thunderstorm
        warnings '''
        feedEntries = []
        self.newEntries = []
        ids = []

        for e in nfeed['entries']:
        ## Only report the SevereThunderStormWarnings
            if e['id'].find('SevereThunderstormWarning') > 0 \
                    or (e.has_key('summary') and e['summary'].find('THUNDERSTORM') > 0):
                feedEntries.append(e)
                newid = e['id'].split('=', 1)[1]
                state = newid[0:2]
                ids.append(newid)
                if newid not in self.shelf["thunderstorm"]:
                    self.newEntries.append(newid)
                    self.shelf["thunderstorm"][newid] = state + ":" + \
                        e["summary"]
                    #self.displayEntry(e)
                    storm=self.recordEntry(e)
                    self.createAlert(storm)
                    self.shelf["thunderstorm"][newid]

        # Clean up the existing entries
        tsIds = self.shelf["thunderstorm"].keys()
        for idx in tsIds:
            if idx not in ids:
                del self.shelf["thunderstorm"][idx]
        self.shelf.sync()

    def summarize(self):
        pass

    def recordEntry(self, e):
        newid = e['id'].split('=', 1)[1]
        state = newid[0:2]
        stormType=StormType.get_by(value ='Thunderstorm')
        sState=StormStates.get_by(value = 'New')
        uState=UnitedStates.get_by(abbreviation = state)
        newStorm=Storm(stormID = newid,
                       stormType = stormType,
                       effective = e['effective'],
                       expires = e['expires'],
                       sevLevel = e['severity'],
                       urgency = e['urgency'],
                       summary = e['summary'],
                       uState = uState,
                       sState = sState)
        newStorm.save_or_update()
        session.commit()
        return newStorm

    def createAlert(self,storm):
        stormState=StormStates.get_by(value = 'Processing')
        storm.sState=stormState
        storm.save_or_update()
        #find all active users following the uState affected by the storm
        tState=TweetStates.get_by(value='New')
        fState=FollowerStates.get_by(value='Active')
        peeps=Follower.query.filter_by(fState=fState)
        peeps=peeps.filter_by(uState=storm.uState)
        #record a tweet for every affected follower
        for aPerson in peeps.all():
            print("Notifying: %s" % aPerson.name)
            newTweet=Tweets(follower=aPerson,
                           storm=storm,tState=tState)
            newTweet.save()
        
        session.commit()
                           
        #after alerting all users, change the stormstate to dispatched so we
        #know we told everyone
        stormState=StormStates.get_by(value = 'Dispatched')
        storm.sState=stormState
        storm.save_or_update()
        session.commit()
