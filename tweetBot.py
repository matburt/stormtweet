from twitter import Twitter
from threading import Timer
from model import *
from sqlalchemy import func

class TweetBot:
    def __init__(self):
        self.tbox=Twitter('stormwarn','st0rmp22wd')
        
    def recordMessage(self, message):
        ### Need to parse the really lame timestamp twitter uses in 'created_at'
        dm=DirectMessages(message['id'])
        ## Expect the message to be  'follow XX'  where XX is a state abbreveation
        action = message['text'].split()[0].lower()
        state = message['text'].split()[1].upper()
        sender = message['sender_screen_name']

        try:
            ustate = UnitedStates.get_by(value=state)
        except StandardError, error:
            print error
            self.tbox.direct_messages.new(sender, 'I am sorry %s , I can not do that.  Please try follow|silence|stop XX' % sender)

        if action == 'follow':
            fstate=FollowerStates.get_by(value='Active')
            Follower.update_or_create(userid=sender, fstate=fstate, ustate=ustate)
            self.tbox.direct_messages.new(sender, 'Congrats! You are now following storms in %s. Silence updates with   silence %s' % (state,state))
        elif action == 'silence':
            fstate=FollowerStates.get_by(value='Slienced')
            Follower.update_or_create(userid=sender, fstate=fstate, ustate=ustate)
            self.tbox.direct_messages.new(sender, 'SHHHHHH.  You have silenced updates for storms in %s. Enable updates with   follow %s' % (state,state))
        elif action == 'stop':
            fstate=FollowerStates.get_by(value='Inactive')
            Follower.update_or_create(userid=sender, fstate=fstate, ustate=ustate)
            self.tbox.direct_messages.new(sender, 'FOR SHAME!  You are no longer following storms in %s. Enable updates with   follow %s' % (state,state))
        else:
            self.tbox.direct_messages.new(sender, 'I am sorry %s , I can not do that.  Please try follow|silence|stop XX' % sender)

            

    def getMessages(self):
        lastMessageID=DirectMessages.query().max(DirectMessages.messageID)
        messages=self.tbox.direct_messages(since_id=lastMessageID)
        print messages
