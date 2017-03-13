from datetime import datetime, timedelta
import json, random
import requests
import tweet_fetcher
from ..models.channel import Channel
from ..models.conference import Conference
from ..models.message import Message
from ..models.tag import Tag, twitter_tags
from .. import app
from utils import calculate_hash
from message_formatter import ask_question, format_conference_data


def send_notification(webhook_url, data):
    headers = {'content-type': 'application/json'}
    try:
        resp = requests.post(webhook_url, headers=headers, data=json.dumps(data))
        if resp.status_code != 200:
            print resp.text
            print "Something went wrong! Unable to send notifications to slack"
            return
    except:
        print "Connection error"
        return
    print "Data sent to ", webhook_url


def is_already_sent(data, channel):
    messages_already_sent = channel.messages.all()
    data_hash = calculate_hash(data)
    hours, minutes, seconds = app.config['SEND_SAME_TWEET_TIMER']
    for message in messages_already_sent:
        if data_hash == message.text_hash:
            if datetime.now() - message.last_sent_on < timedelta(hours=hours, minutes=minutes, seconds=seconds):
                print "Message was recently sent to the channel"
                return True
    return False


def is_subscribed(channel, tag):
    if tag is None: return True
    return channel.tags.all().count(tag) > 0


def send_to_channel(channel, data, tag=None):
    if not is_already_sent(data, channel) and is_subscribed(channel, tag):
        print "Sending to : ", channel.channel_name
        send_notification(channel.incoming_webhook_url, data)
        message = Message(data, datetime.now(), channel.id)
        message.save()
    else:
        print "Message already sent to the channel"


def send_to_all_channels(data, tag=None):
    channels = Channel.query.all()
    for channel in channels:
        send_to_channel(channel, data, tag)


def send_tweets():
    print "Sending tweets"
    tweet, tag = tweet_fetcher.get_most_retweeted()
    response = {'attachments': []}
    print "Sending tweet : ", tag, tweet
    data = {'pretext': '*Some trending news about conferences*', 'mrkdwn_in': ['text', 'pretext'],
            'title': 'Happening on twitter', 'text': tweet, 'color': '#36a64f'}
    response['attachments'].append(data)
    send_to_all_channels(response, tag)


def send_upcoming_conference_notification():
    upcoming_conferences = Conference.fetch_upcoming_conferences()
    formatted_data = format_conference_data(upcoming_conferences)
    if formatted_data:
        send_to_all_channels(formatted_data)


def get_slack_details():
    channels = Channel.query.all()
    data = ''
    for channel in channels:
        data += str(channel) + "<br><br>"
    return data


def give_suggestions(channel):
    tag_names = twitter_tags.keys()
    random.shuffle(tag_names)
    tags_to_send = []
    for tag_name in tag_names[:3]:
        print "TAG NAME: ", tag_name
        tag = Tag.query.filter_by(name=tag_name).first()
        if not is_subscribed(channel, tag):
            print "Not subscribed to :", tag
            tags_to_send.append(tag_name.capitalize())
        else:
            print "Already subscribed"

    if len(tags_to_send) > 0:
        data = ask_question('Are you finding this information useful?', tags_to_send)
        send_to_channel(channel, data)
    else:
        data = 'Channel already subscribed to all tags'
    return data


def give_tag_suggestion_to_all():
    channels = Channel.query.all()
    for channel in channels:
        give_suggestions(channel)
