import requests, time, json
from ..models.slackinfo import SlackInfo

def send_notification(webhook_url, data):
	headers = {'content-type': 'application/json'}

	resp = requests.post(webhook_url, headers=headers, data=json.dumps(data))
	if resp.status_code != 200:
		print "Something went wrong! Unable to send notifications to slack"
	print "Data send to ", webhook_url


def send_to_all_channels(data):
	channels = SlackInfo.query.all()
	for channel in channels:
		print "Sending to : ", channel.channel_name 
		send_notification(channel.incomming_webhook_url, data)


def notify_all():
	data = {'text' : "Time in my clock is :" + time.strftime('%X %x %Z')}
	send_to_all_channels(data)