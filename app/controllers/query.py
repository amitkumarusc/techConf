from .. import app, db
import os
import json
from difflib import SequenceMatcher
from flask import request, Response
from ..models.conference import Conference

conferences = []

def similar(a, b):
	return SequenceMatcher(None, a, b).ratio()

def parse_parameters(parameters):
	parameters = parameters.split(' ')
	token = ""
	for parameter in parameters:
		if parameter.startswith('-') or parameter.startswith('/'):
			parameter = parameter.strip('-')
			parameter = parameter.strip('/')


def search_conferences(user_id, command_options):
	response = {}
	response['attachments'] = []
	pretext = True
	conferences = Conference.query.all()
	print dir(conferences[0])
	for conference in conferences:
		data = {}
		ratio = similar(command_options, conference.location.lower())
		if ratio > 0.5:
			data['title'] = conference.name
			data['text'] = 'Date : %s to %s\nLocation : %s\nDescription : %s'%(conference.start_date.date(), conference.end_date.date(),conference.location,conference.desc)
			data['title_link'] = conference.url
			data['color'] = '#36a64f'
			if pretext:
				data['pretext'] = "*Hi <@" + user_id + ">! "
				data['mrkdwn_in'] = ['text', 'pretext']
				data['pretext'] += "Some of the conferences I managed to find!*"
				pretext = False

			response['attachments'].append(data)


	if len(response['attachments']) == 0:
		data = {}
		data['color'] = '#e60000'
		data['pretext'] = "*Hi <@" + user_id + ">! Could not able to find any conferences for that region*"
		response['attachments'].append(data)
	return response


@app.route('/command', methods=['POST'])
def command():
	user_id = request.form['user_id']
	command_options = request.form['text'].lower()

	response = search_conferences(user_id, command_options)

	js = json.dumps(response)
	resp = Response(js, status=200, mimetype='application/json')

	return resp
