import twitter, os

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token_key = os.environ['ACCESS_TOKEN_KEY']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

twitter_channels = ['@rubyconf', '@rubyconfindia']


def get_most_retweeted():
    tweets = []
    for channel in twitter_channels:
        tweets.extend(api.GetUserTimeline(screen_name=channel))

    formatted = []
    for tweet in tweets:
        formatted.append((tweet.retweet_count, tweet.text))

    formatted.sort(key=lambda x: x[0])
    formatted.reverse()
    return formatted[0][1].replace("RT @", "@")


if __name__ == "__main__":
    print get_most_retweeted()