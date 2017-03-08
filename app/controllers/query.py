import json
from flask import request, Response

from .. import app
from ..models.conference import Conference
from ..utils.notifier import format_conference_data

SWITCH = True


def parse_parameters(parameters):
    options = {'more': None}
    temp = parameters.split("-", 1)
    if len(temp) == 2:
        parameters = '-' + temp[1].strip()

    location = temp[0].strip()

    options['location'] = location

    options['more'] = 0
    options['all'] = False

    for parameter in parameters.split(' '):
        if parameter.startswith('-'):
            parameter = parameter.strip('-')
            flag_array = parameter.split('=')
            parameter = flag_array[0].strip()
            if len(flag_array) == 1:
                parameter_val = True
            else:
                parameter_val = flag_array[1].strip()
            options[parameter] = parameter_val

    options['more'] = int(options['more'])

    print options
    return options


def usage_response():
    response = {}
    response['attachments'] = []
    data = {}
    data['pretext'] = '*Basic command to use this app are listed below*'
    data['mrkdwn_in'] = ['text', 'pretext']
    data['title'] = 'Fetch conferences in a region/city'
    data['text'] = '/techConf city_name\n'
    data['text'] += 'Example :\n'
    data['text'] += '/techConf Bangalore'
    data['color'] = '#36a64f'

    response['attachments'].append(data)

    data = {}
    data['title'] = 'Fetch more conferences in a region/city'
    data['text'] = '/techConf city_name -more=[page_number]\n'
    data['text'] += 'Example :\n'
    data['text'] += '/techConf Bangalore -more=1\n'
    data['text'] += '/techConf Bangalore -more=2'
    data['color'] = '#36a64f'

    response['attachments'].append(data)

    data = {}
    data['title'] = 'Fetch conferences in a region/city and notify all'
    data['text'] = '/techConf city_name -all\n'
    data['text'] += 'Example :\n'
    data['text'] += '/techConf Bangalore -all'
    data['color'] = '#36a64f'

    response['attachments'].append(data)
    return response


@app.route('/command', methods=['POST'])
def command():
    user_id = request.form['user_id']
    command_options = request.form['text'].lower()
    if command_options == '':
        response = usage_response()
    else:
        options = parse_parameters(command_options)
        conferences = Conference.fetch_all_conferences(query=options['location'])
        response = format_conference_data(conferences, user_id=user_id, page=options['more'], per_page=5,
                                          notify_all=options['all'])

    js = json.dumps(response)
    resp = Response(js, status=200, mimetype='application/json')

    return resp
