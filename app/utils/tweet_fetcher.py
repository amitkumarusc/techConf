import twitter

consumer_key = 'ghR96YyXAGb4tvdujdybxONST'
consumer_secret = 'X3HqKxnplwKQI425S5bZmiB8jBVnZ94MdXdfva1g8R4ptczlU1'
access_token_key = '501890611-8yfgTC3Jm72Wcz7rJZxkGW3DKDY2Bfz3rnJQbBF6'
access_token_secret = 'NIOn9eMBneqIfiiTIrpXy4clIcu30S1vb5cGd8fZj9Mbv'

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