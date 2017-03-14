import twitter, os
from datetime import datetime
from ..models.tag import Tag
import random

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token_key = os.environ['ACCESS_TOKEN_KEY']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)


def get_most_retweeted_by_channel(channel):
    tweets = api.GetUserTimeline(screen_name=channel)
    formatted = []
    for tweet in tweets:
        time = tweet.created_at.split(' ')
        time.pop(4)
        time = ' '.join(time)
        datetime_object = datetime.strptime(time, '%a %b %d %H:%M:%S %Y')
        formatted.append((tweet.retweet_count, datetime_object, tweet.text.encode('utf-8')))

    formatted.sort(key=lambda x: (x[0], x[1]))
    formatted.reverse()
    return formatted[0][2].replace("RT @", "@")


def get_most_retweeted():
    tags = Tag.query.all()
    print "TAGS are: ", tags
    tag = random.choice(tags)
    return get_most_retweeted_by_channel(tag.twitter_handle), tag


if __name__ == "__main__":
    print get_most_retweeted()
