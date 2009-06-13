import feedparser
import shelve
import re

class ThunderStorm(object):
    '''ThunderStorm class used to parse and store relevant information
    for a Severe ThunderStorm Alert'''
    def __init__(self, feedUrl, shelfPath):
        #self.order=['location','effective','direction','expires','rain',
        #            'winds','lightining','hail']
        self.shelf = shelve.open(shelfPath, writeback=True)
        if "thunderstorm" not in self.shelf:
            self.shelf["thunderstorm"] = {}
        self.parse(feedparser.parse(feedUrl))

    def displayEntry(self, entry):
        id = entry['id'].split('=', 1)[1]
        state = id[0:2]
        sevLevel = entry['cap_severity']
        effective = entry['cap_effective']
        expires = entry['cap_expires']
        urgency = entry['cap_urgency']
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
            if e['id'].find('SevereThunderstormWarning') > 0:
                feedEntries.append(e)
                newid = e['id'].split('=', 1)[1]
                state = newid[0:2]
                ids.append(newid)
                if newid not in self.shelf["thunderstorm"]:
                    self.newEntries.append(newid)
                    self.shelf["thunderstorm"][newid] = state + ":" + \
                        e["summary"]
                    self.displayEntry(e)
                    storm=self.recordEntry(e)
                    self.alertOnStorm(storm)
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
        stormType=StormType.get_by(value ='Thunderstorm')
        stormState=StormStates.get_by(value = 'New')
        uState=UnitedStates.get_by(abbreviation = e['id'][0:2])
        newStorm=Storm(stormID = e['id'],
                       stormType = stormType,
                       effective = e['cap_effective'],
                       expires = e['cap_expires'],
                       sevLevel = e['cap_severity'],
                       urgency = e['cap_urgency'],
                       summary = e['summary'],
                       uState = uState,
                       sState = sState)
        newStorm.update_or_save()
        return newStorm

    def alertOnStorm(self,storm):
        # this whole function may need to run as a separate thread
        # instead of inline with the rss parsing

        # change the state to proccessing until we finish sending the alerts
        stormState=StormStates.get_by(value = 'Processing')
        storm.sState=stormState
        storm.update_or_save()
        #find all active users following the uState affected by the storm

        # for each active user
        # send a direct message to each user
        #record the tweet sent to each user

        #after alerting all users, change the stormstate to dispatched so we
        #know we told everyone
