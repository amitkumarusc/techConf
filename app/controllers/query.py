from .. import app, db
import os, re
import json
from flask import request, Response
from ..utils.notifier import format_conference_data
from ..models.conference import Conference


def parse_parameters(parameters):
	options = {'more' : None}
	location = re.findall(r'"([^"]*)"', parameters)
	temp = parameters.split("-", 1)
	if len(temp) == 2:
		parameters = '-' + temp[1].strip()

	location = temp[0].strip()

	options['location'] = location

	options['more'] = 0

	for parameter in parameters.split(' '):
		if parameter.startswith('-'):
			parameter = parameter.strip('-')
			parameter, parameter_val = parameter.split('=')
			options[parameter] = parameter_val

	options['more'] = int(options['more'])

	print options
	return options

@app.route('/command', methods=['POST'])
def command():
	user_id = request.form['user_id']
	command_options = request.form['text'].lower()
	options = parse_parameters(command_options)
	conferences = Conference.fetch_from_location(options['location'])
	response = format_conference_data(conferences, user_id=user_id, page=options['more'], per_page=5)

	js = json.dumps(response)
	resp = Response(js, status=200, mimetype='application/json')

	return resp
