import requests, time, json, os
from datetime import datetime
from ..models.slackinfo import SlackInfo

from flask import request, Response
from ..models.conference import Conference

def format_conference_data(conferences, user_id=None, page=0, per_page=3, notify_all=False):
	response = {}
	response['attachments'] = []
	if notify_all:
		response['response_type'] = 'in_channel'
	pretext = True
	#conferences = Conference.query.all()
	index = 0
	for conference in conferences:
		data = {}

		if index <= page*per_page:
			index += 1
			continue
		if index > (page+1)*per_page:
			break
		index += 1

		data['title'] = conference.name
		data['text'] = 'Date : %s to %s\nLocation : %s\nDescription : %s'%(conference.start_date.date(), conference.end_date.date(),conference.location,conference.desc)
		data['title_link'] = conference.url
		data['color'] = '#36a64f'
		if pretext:
			if user_id:
				data['pretext'] = "*Hi <@" + user_id + ">! Some of the conferences I managed to find!*"
			else:
				data['pretext'] = "*Conferences in database*"
			data['mrkdwn_in'] = ['text', 'pretext']
			pretext = False
		response['attachments'].append(data)


	if len(response['attachments']) == 0:
		if user_id==None:
			return None
		data = {}
		data['color'] = '#e60000'
		data['pretext'] = "*Hi <@" + user_id + ">! Could not able to find any conferences for that region*"
		response['attachments'].append(data)
	return response


def send_notification(webhook_url, data):
	headers = {'content-type': 'application/json'}
	try:
		resp = requests.post(webhook_url, headers=headers, data=json.dumps(data))
		if resp.status_code != 200:
			print "Something went wrong! Unable to send notifications to slack"
			return
	except:
		print "Connection error"
		return
	print "Data sent to ", webhook_url


def send_to_all_channels(data):
	channels = SlackInfo.query.all()
	for channel in channels:
		print "Sending to : ", channel.channel_name 
		send_notification(channel.incomming_webhook_url, data)


def notify_all():
	upcoming_conferences = Conference.fetch_upcoming_conferences(datetime.now().date())
	formatted_data = format_conference_data(upcoming_conferences)
	if formatted_data:
		#data = {'text' : "Time in my clock is :" + time.strftime('%X %x %Z')}
		send_to_all_channels(formatted_data)



