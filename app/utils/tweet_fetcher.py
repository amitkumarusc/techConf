import twitter, os
from datetime import datetime

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token_key = os.environ['ACCESS_TOKEN_KEY']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

twitter_channels = ['@rubyconf', '@rubyconfindia'] #['@GeekAmitYadav']


def get_most_retweeted():
    tweets = []
    for channel in twitter_channels:
        tweets.extend(api.GetUserTimeline(screen_name=channel))

    formatted = []
    for tweet in tweets:
        time = tweet.created_at.split(' ')
        time.pop(4)
        time = ' '.join(time)
        datetime_object = datetime.strptime(time, '%a %b %d %H:%M:%S %Y')
        formatted.append((tweet.retweet_count, datetime_object, tweet.text))

    formatted.sort(key=lambda x: (x[0], x[1]))
    formatted.reverse()
    return formatted[0][2].replace("RT @", "@")


if __name__ == "__main__":
    print get_most_retweeted()