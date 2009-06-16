from twitter import Twitter
from model import *

class TweetBox:
    def __init__(self, user, password):
        self.tbox=Twitter(user, password)

    def stormMessage(message, receipients):
        for aUser in receipients:
            self.tbox.direct_messages.new(user=aUser,text=message)

    def update(message):
        self.tbox.statuses.update(status='message')
