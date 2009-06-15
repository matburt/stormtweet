from twitter import Twitter
import time
from model import *
from sqlalchemy import func
from ConfigParser import RawConfigParser
import optparse

SORRY_MSG = """
I am sorry %s , I can not do that.  Please try follow|silence|stop XX
"""
FOLLOW_SUCCESS_MSG = """
Congrats! You are now following storms in %s. Silence updates with: silence %s
"""
SILENCE_SUCCESS_MSG = """
SHHHHHH.  You have silenced updates for storms in %s. Enable
 updates with: follow %s
"""
STOP_SUCCESS_MSG = """
FOR SHAME!  You are no longer following storms in %s. Enable updates with:
 follow %s
"""
UNKNOWN_MSG = """
I am sorry %s , I can not do that.  Please try follow|silence|stop XX
"""
FOLLOWING_MSG = """
Thanks for following StormWarn! To get storm warnings for a state with postal
 abbreviation XX send me:\nfollow XX to get updates
"""
# setup the model
setup_all()

class TweetBot:
    def __init__(self, tUser, tPassword):
        self.tbox = Twitter(tUser, tPassword)

    def recordMessage(self, message):
        # Need to parse the really lame timestamp twitter uses in 'created_at'
        dm = DirectMessages(messageID = message['id'])
        # Expect the message to be  'follow XX'  where XX is a state
        # abbreveiation
        action = message['text'].split()[0].lower()
        state = message['text'].split()[1].upper()
        sender = message['sender_screen_name']

        follower=Follower.get_by(userid = sender)
        if not follower:
            follower=Follower(userid = sender)
            session.commit()

        ustate = UnitedStates.get_by(value=state)
        if not ustate:
            self.tbox.direct_messages.new(user = sender,
                                          text=SORRY_MSG % sender)

        if action == 'follow':
            fstate = FollowerStates.get_by(value='Active')
            follower.fState = fstate
            follower.uState = ustate
            follower.update()
            self.tbox.direct_messages.new(user = sender,
                                          text = FOLLOW_SUCCESS_MSG %
                                          (state,state))
        elif action == 'silence':
            fstate = FollowerStates.get_by(value='Slienced')
            follower.fState = fstate
            follower.uState = ustate
            follower.update()
            self.tbox.direct_messages.new(user = sender,
                                          text = SILENCE_SUCCESS_MSG %
                                          (state,state))
        elif action == 'stop':
            fstate = FollowerStates.get_by(value='Inactive')
            follower.fState = fstate
            follower.uState = ustate
            follower.update()
            self.tbox.direct_messages.new(user = sender,
                                          text = STOP_SUCCESS_MSG %
                                          (state,state))
        else:
            self.tbox.direct_messages.new(user = sender,
                                          text = UNKNOWN_MSG % sender)

        session.commit()


    def getMessages(self):
        lastMessageID = DirectMessages.query().max(DirectMessages.messageID)
        messages = self.tbox.direct_messages(since_id = lastMessageID)
        for aMessage in messages:
            self.recordMessage(aMessage)


    def makeFriends(self):
        currentFriends=set(self.tbox.friends.ids.stormwarn())
        followers=set(self.tbox.followers.ids.stormwarn())
        newFriends=followers - currentFriends
        for aFriend in newFriends:
            self.tbox.friendships.create(id=aFriend)
            screen_name=self.tbox.users.show(id = aFriend)['screen_name']
            self.tbox.direct_messages.new(user = screen_name,
                                          text = FOLLOWING_MSG)
        session.commit()

    def doit(self):
        self.makeFriends()
        self.getMessages()

def getConfig(path): # move into common module with stormtweet.getConfig
    rc = RawConfigParser()
    if path not in rc.read(path):
        print("Invalid Configuration File")
        sys.exit(1)
    return rc

def getOptions():
    op = optparse.OptionParser()
    op.add_option("-c", "--config", dest="config",
                  help="configuration file")
    op.add_option("-i", "--initialize", dest="initialize",
                  help="Initialize database, don't actually post entries")
    op.add_option("-v", "--verbose", dest="verbose",
                  help="Display extra information")
    (options, args) = op.parse_args()

    if options.config is None:
        print("Configuration file required")
        sys.exit(1)

    return (options, args)

def main():
    options, args = getOptions()
    config = getConfig(options.config)
    spam=TweetBot(config.get("tweetbox", "user"),
                  config.get("tweetbox", "password"))

    while 1:
        spam.doit()
        print 'sleeping ....'
        time.sleep(1800)

if __name__=='__main__':
    main()
