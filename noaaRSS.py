import feedparser
import re

## Main URL for NOAA's RSS feed
NOAARSSURL='''http://www.weather.gov/alerts-beta/us.php?x\x3d0'''

## Build a feed parser for the NOAA RSS feed
noaaFeed=feedparser.parse(NOAARSSURL)


class ThunderStorm(object):
    '''ThunderStorm class used to parse and store relevant information
    for a Severe ThunderStorm Alert'''
    def __init__(self, feedEntry):
        ## Feed information
        self.id=None
        self.state=None
        self.sevLevel=None
        self.urgency=None
        self.effective=None
        self.expires=None
        self.summary=None
        self.areas=None
        ## Storm Information
        self.hail=None
        self.lightining=None
        self.winds=None
        self.rain=None
        self.location=None
        self.direction=None
        ## Twitter Information
        self.tweet=None
        self.order=['location','effective','direction','expires','rain','winds','lightining','hail']
        self.parse(feedEntry)

    def parse(self, nfeed):
        ''' Trip through the feed entries and print the thunderstorm warnings '''
        for e in nfeed['entries']:
        ## Only report the SevereThunderStormWarnings
            if e['id'].find('SevereThunderstormWarning')>0:
                ## split the url on the equal sign and grab what comes after it
                self.id=e['id'].split('=')[1]
                self.state=id[0:2]
                self.sevLevel=e['cap_severity']
                self.effective=e['cap_effective']
                self.expires=e['cap_expires']
                self.urgency=e['cap_urgency']
                self.summary=e['summary']
                print "========================================"
                print "ID:            %s" % self.id
                print "State:         %s" % self.state
                print "Severity:      %s" % self.sevLevel
                print "Urgency:       %s" % self.urgency
                print "Effective:     %s" % self.effective
                print "Expires:       %s" % self.expires
                print "Summary:       %s" % self.summary
                print "========================================"
                
    def summarize(self):
        pass



