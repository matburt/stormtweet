from twitter import Twitter
import optparse
import sys
from ConfigParser import RawConfigParser
from model import *

class TweetBox:
    def __init__(self, user, password, modelBind):
        self.tbox=Twitter(user, password)
        setupModel(modelBind)

    def stormMessage(self, message, receipient):
        self.tbox.direct_messages.new(user=receipient,text=message)

    def update(self, message):
        self.tbox.statuses.update(status='message')

    def getAlerts(self):
        tState=TweetStates.get_by(value='New')
        success=TweetStates.get_by(value='Successful')
        error=TweetStates.get_by(value='Error')
        tweets=Tweets.query.filter_by(tState=tState)
        for t in tweets.all():
            print t.follower.name, t.storm.id
            try:
                self.stormMessage(t.storm.summary,
                                  t.follower.name)
                t.tState=success
                t.update()
            except StandardError, e:
                print e
                t.tState=error
                t.update()
        session.commit()

def getConfig(path):
    rc = RawConfigParser()
    if path not in rc.read(path):
        print("Invalid Configuration File")
        sys.exit(1)
    return rc

def main():
    op = optparse.OptionParser()
    op.add_option("-c", "--config", dest="config",
                  help="configuration file")
    op.add_option("-i", "--initialize", dest="initialize",
                  help="Initialize database, don't actually post entries",
                  action="store_true", default=False)
    op.add_option("-v", "--verbose", dest="verbose",
                  help="Display extra information",
                  action="store_true", default=False)
    (options, args) = op.parse_args()

    if options.config is None:
        print("Configuration file required")
        sys.exit(1)

    config = getConfig(options.config)

    tbox = TweetBox(config.get("tweetbox", "user"),
                    config.get("tweetbox", "password"),
                    config.get("model", "bind"))
    tbox.getAlerts()

if __name__ == '__main__':
    main()
    
