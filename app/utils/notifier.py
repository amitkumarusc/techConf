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


class Priority(object):
    ULTRA_HIGH = 20
    SUPER_HIGH = 15
    HIGH = 10
    MEDIUM = 5
    LOW = 0


def send_notification(webhook_url, data):
    headers = {'content-type': 'application/json'}
    try:
        resp = requests.post(webhook_url, headers=headers, data=json.dumps(data))
        if resp.status_code != 200:
            print resp.text
            print "Something went wrong! Unable to send notifications to slack\n\n"
            return
    except:
        print "Connection error\n\n"
        return
    print "Data sent to ", webhook_url, "\n\n"


def need_to_send(time_diff, priority):
    time_condition = time_diff > timedelta(days=30)
    if time_condition: return True
    time_condition = time_diff > timedelta(days=7)
    if time_condition and priority == Priority.MEDIUM: return True
    time_condition = time_diff > timedelta(days=2)
    if time_condition and priority == Priority.HIGH: return True
    time_condition = time_diff > timedelta(days=1)
    if time_condition and priority == Priority.SUPER_HIGH: return True
    if priority == Priority.ULTRA_HIGH: return True
    return False


def is_already_sent(data, channel, priority=Priority.LOW):
    messages_already_sent = channel.messages.all()
    data_hash = calculate_hash(data)
    for message in messages_already_sent:
        if data_hash == message.text_hash:
            time_difference = datetime.now() - message.last_sent_on
            if not need_to_send(time_difference, priority):
                print "Message was recently sent to the channel"
                return True
    return False


def is_subscribed(channel, tag):
    if tag is None: return True
    return channel.tags.all().count(tag) > 0


def send_to_channel(channel, data, tag=None, priority=Priority.LOW):
    if not is_already_sent(data, channel, priority=priority) and is_subscribed(channel, tag):
        print "Sending to : ", channel.channel_name
        send_notification(channel.incoming_webhook_url, data)
        message = Message(data, datetime.now(), channel.id)
        message.save()
    else:
        print "Message already sent to the channel or channel not subscribed to tag\n\n"


def send_to_all_channels(data, tag=None, priority=Priority.LOW):
    channels = Channel.query.all()
    for channel in channels:
        send_to_channel(channel, data, tag, priority=priority)


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
        tag = Tag.query.filter_by(name=tag_name).first()
        if not is_subscribed(channel, tag):
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


def send_upcoming_conference_notification():
    priority = Priority.SUPER_HIGH
    upcoming_conferences = Conference.fetch_next_day_conferences()
    if len(upcoming_conferences) != 0:
        print "There are some conferences for tomorrow"
    if len(upcoming_conferences) == 0:
        print "No conferences tomorrow"
        upcoming_conferences = Conference.fetch_next_two_days_conferences()
        priority = Priority.HIGH
    if len(upcoming_conferences) == 0:
        print "No conferences in next two days"
        upcoming_conferences = Conference.fetch_next_week_conferences()
        priority = Priority.MEDIUM
    if len(upcoming_conferences) == 0:
        print "No conferences next week"
        upcoming_conferences = Conference.fetch_upcoming_conferences()
        priority = Priority.LOW
    formatted_data = format_conference_data(upcoming_conferences)
    if formatted_data:
        send_to_all_channels(formatted_data, priority=priority)


def send_tweets():
    print "Sending tweets"
    tweet, tag = tweet_fetcher.get_most_retweeted()
    response = {'attachments': []}
    print "Sending tweet : ", tag, tweet
    data = {'pretext': '*Some trending news about conferences*', 'mrkdwn_in': ['text', 'pretext'],
            'title': 'Happening on twitter', 'text': tweet, 'color': '#36a64f'}
    response['attachments'].append(data)
    send_to_all_channels(response, tag, priority=Priority.MEDIUM)