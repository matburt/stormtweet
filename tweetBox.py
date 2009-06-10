from twitter import Twitter

##tbox=Twitter('stormwarn','st0rmp22wd')

##tbox.statuses.update(status='testing python call')

def stormMessage(message, receipients):
    tbox=Twitter('stormwarn','st0rmp22wd')
##    tbox.direct_messages.new(user='timothy_edwards',text=message)
    for aUser in receipients:
        tbox.direct_messages.new(user=aUser,text=message)


def update(message):
    tbox=Twitter('stormwarn','st0rmp22wd')
    tbox.statuses.update(status='message')
