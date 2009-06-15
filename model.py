from elixir import *
import mx.DateTime

## Set the data base backend (maybe pgsql later?)
metadata.bind = "postgres://stormtweet:270rm@localhost/stormtweet"
## Debug SQL for now
metadata.bind.echo = True


class StormType(Entity):
    value = Field(String(20))

class UnitedStates(Entity):
    abbreviation = Field(String(2), synonym='value')
    name = Field(String(15))

class StormStates(Entity):
    value = Field(String(20))

class TweetStates(Entity):
    value = Field(String(20))

class FollowerStates(Entity):
    value = Field(String(20))

class Storm(Entity):
    stormType = ManyToOne('StormType') ## Hurricane, Thunderstorm, Tornado, Blizzard, etc
    stormID = Field(String(256))
    effective = Field(DateTime, synonym='start')
    expires = Field(DateTime, synonym='end')
    sevLevel = Field(String(20))  ## NOAA severity level
    urgency = Field(String(20))  ## NOAA urgency level
    summary = Field(Text, synonym='s')
    uState = ManyToOne('UnitedStates')
    sState = ManyToOne('StormStates')


class Follower(Entity):
    userid = Field(String(50),synonym='name')
    uState = ManyToOne('UnitedStates')
    fState = ManyToOne('FollowerStates')
    joinedDate = Field(DateTime, default = mx.DateTime.now)
    modified = Field(DateTime, default = mx.DateTime.now)

class Tweets(Entity):
    follower = ManyToOne('Follower')
    storm = ManyToOne('Storm')
    tState = ManyToOne('TweetStates')


class DirectMessages(Entity):
    messageID = Field(String(50))
    messageTime = Field(DateTime, default = mx.DateTime.now)


def createDataBase():
    setup_all()
    create_all()

    ## Make the Storms
    StormType(value='Thunderstorm')
    StormType(value='Hurricane')
    StormType(value='Tropical Depression')
    StormType(value='Tornado')
    StormType(value='Blizzard')

    ## Make the storm and tweet states
    StormStates(value='New')
    StormStates(value='Processing')
    StormStates(value='Dispatched')

    TweetStates(value='New')
    TweetStates(value='Successful')
    TweetStates(value='Error')
    
    FollowerStates(value='Active')
    FollowerStates(value='Silenced')
    FollowerStates(value='Inactive')

    UnitedStates(value='AL', name='Alabama')
    UnitedStates(value='AK', name='Alaska')
    UnitedStates(value='AZ', name='Arizona')
    UnitedStates(value='AR', name='Arkansas')
    UnitedStates(value='CA', name='California')
    UnitedStates(value='CO', name='Colorado')
    UnitedStates(value='CT', name='Connecticut')
    UnitedStates(value='DE', name='Delaware')
    UnitedStates(value='FL', name='Florida')
    UnitedStates(value='GA', name='Georgia')
    UnitedStates(value='HI', name='Hawaii')
    UnitedStates(value='ID', name='Idaho')
    UnitedStates(value='IL', name='Illinois')
    UnitedStates(value='IN', name='Indiana')
    UnitedStates(value='IA', name='Iowa')
    UnitedStates(value='KS', name='Kansas')
    UnitedStates(value='KY', name='Kentucky')
    UnitedStates(value='LA', name='Louisiana')
    UnitedStates(value='ME', name='Maine')
    UnitedStates(value='MD', name='Maryland')
    UnitedStates(value='MA', name='Massachusetts')
    UnitedStates(value='MI', name='Michigan')
    UnitedStates(value='MN', name='Minnesota')
    UnitedStates(value='MS', name='Mississippi')
    UnitedStates(value='MO', name='Missouri')
    UnitedStates(value='MT', name='Montana')
    UnitedStates(value='NE', name='Nebraska')
    UnitedStates(value='NV', name='Nevada')
    UnitedStates(value='NH', name='New Hampshire')
    UnitedStates(value='NJ', name='New Jersey')
    UnitedStates(value='NM', name='New Mexico')
    UnitedStates(value='NY', name='New York')
    UnitedStates(value='NC', name='North Carolina')
    UnitedStates(value='ND', name='North Dakota')
    UnitedStates(value='OH', name='Ohio')
    UnitedStates(value='OK', name='Oklahoma')
    UnitedStates(value='OR', name='Oregon')
    UnitedStates(value='PA', name='Pennsylvania')
    UnitedStates(value='RI', name='Rhode Islan')
    UnitedStates(value='SC', name='South Carolina')
    UnitedStates(value='SD', name='South Dakota')
    UnitedStates(value='TN', name='Tennessee')
    UnitedStates(value='TX', name='Texas')
    UnitedStates(value='UT', name='Utah')
    UnitedStates(value='VT', name='Vermont')
    UnitedStates(value='VA', name='Virginia')
    UnitedStates(value='WA', name='Washington')
    UnitedStates(value='WV', name='West Virginia')
    UnitedStates(value='WI', name='Wisconsin')
    UnitedStates(value='WY', name='Wyoming')    
    
    session.commit()
