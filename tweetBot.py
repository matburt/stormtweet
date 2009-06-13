from twitter import Twitter
import time
from model import *
from sqlalchemy import func

## setup the model
setup_all()

class TweetBot:
    def __init__(self):
        self.tbox=Twitter('stormwarn','st0rmp22wd')
        
    def recordMessage(self, message):
        ### Need to parse the really lame timestamp twitter uses in 'created_at'
        dm=DirectMessages(messageID=message['id'])
        ## Expect the message to be  'follow XX'  where XX is a state abbreveation
        action = message['text'].split()[0].lower()
        state = message['text'].split()[1].upper()
        sender = message['sender_screen_name']
        
        follower=Follower.get_by(userid=sender)
        if not follower:
            follower=Follower(userid=sender)
            session.commit()

        ustate = UnitedStates.get_by(value=state)
        if not ustate:
            self.tbox.direct_messages.new(user=sender, text='I am sorry %s , I can not do that.  Please try follow|silence|stop XX' % sender)

        if action == 'follow':
            fstate=FollowerStates.get_by(value='Active')
            follower.fState=fstate
            follower.uState=ustate
            follower.update()
            self.tbox.direct_messages.new(user=sender, text='Congrats! You are now following storms in %s. Silence updates with   silence %s' % (state,state))
        elif action == 'silence':
            fstate=FollowerStates.get_by(value='Slienced')
            follower.fState=fstate
            follower.uState=ustate
            follower.update()
            self.tbox.direct_messages.new(user=sender, text='SHHHHHH.  You have silenced updates for storms in %s. Enable updates with   follow %s' % (state,state))
        elif action == 'stop':
            fstate=FollowerStates.get_by(value='Inactive')
            follower.fState=fstate
            follower.uState=ustate
            follower.update()
            self.tbox.direct_messages.new(user=sender, text='FOR SHAME!  You are no longer following storms in %s. Enable updates with   follow %s' % (state,state))
        else:
            self.tbox.direct_messages.new(user=sender, text='I am sorry %s , I can not do that.  Please try follow|silence|stop XX' % sender)
        
        session.commit()
            

    def getMessages(self):
        lastMessageID=DirectMessages.query().max(DirectMessages.messageID)
        messages=self.tbox.direct_messages(since_id=lastMessageID)
        for aMessage in messages:
            self.recordMessage(aMessage)


    def makeFriends(self):
        currentFriends=set(self.tbox.friends.ids.stormwarn())
        followers=set(self.tbox.followers.ids.stormwarn())
        newFriends=followers - currentFriends
        for aFriend in newFriends:
            self.tbox.friendships.create(id=aFriend)
            screen_name=self.tbox.users.show(id=aFriend)['screen_name']
            self.tbox.direct_messages.new(user=screen_name, text='''Thanks for following StormWarn! To get storm warnings for a state with postal abbreviation XX send me:\nfollow XX to get updates''')
        session.commit()
    def doit(self):
        self.makeFriends()
        self.getMessages()



if __name__=='__main__':
    spam=TweetBot()

    while 1:
        spam.doit()
        print 'sleeping ....'
        time.sleep(1800)

            
