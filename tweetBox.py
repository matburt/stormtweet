from twitter import Twitter
from model import *
xs

class TweetBox:
    def __init__(self, user, password):
        self.tbox=Twitter(user, password)

    def stormMessage(message, receipients):
        tbox=Twitter('stormwarn','st0rmp22wd')
        for aUser in receipients:
            tbox.direct_messages.new(user=aUser,text=message)

    def update(message):
        tbox=Twitter('stormwarn','st0rmp22wd')
        tbox.statuses.update(status='message')
