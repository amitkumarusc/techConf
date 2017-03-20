from .. import app


def ask_question(question, tags):
    response = {'text': '*%s*' % question, 'attachments': []}
    data = {}
    data['mrkdwn_in'] = ['text', 'pretext']

    data['text'] = 'Choose other technologies you are interested in'
    data['fallback'] = 'You are unable to subscribe for a technology'
    data['callback_id'] = 'tech_subs'
    data['color'] = '#3AA3E3'
    data['attachment_type'] = 'default'
    data['actions'] = []

    for tag in tags:
        button = {}
        button['name'] = 'technology'
        button['text'] = tag
        button['type'] = 'button'
        button['value'] = tag.lower()

        data['actions'].append(button)

    button_not_interested = {}
    button_not_interested['name'] = 'technology'
    button_not_interested['text'] = 'Not Interested'
    button_not_interested['type'] = 'button'
    button_not_interested['style'] = 'danger'
    button_not_interested['value'] = 'not_interested'
    button_not_interested['confirm'] = {'title': 'Are you sure?',
                                        'text': "Wouldn't you prefer to get technology updates?", 'ok_text': 'Yes',
                                        'dismiss_text': 'No'}

    data['actions'].append(button_not_interested)

    response['attachments'].append(data)

    return response


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


def format_conference_data(conferences, user_id=None, page=0, per_page=1, notify_all=False):
    response = {}
    response['attachments'] = []
    if notify_all:
        response['response_type'] = 'in_channel'
    pretext = True
    index = 0
    for conference in conferences:
        data = {}

        if index < page * per_page:
            index += 1
            continue
        if index > (page + 1) * per_page:
            break
        index += 1

        data['title'] = conference.name
        data['text'] = 'Date : %s to %s\nLocation : %s\nDescription : %s' % (
            conference.start_date.date(), conference.end_date.date(), conference.location, conference.desc)
        data['title_link'] = conference.url
        data['color'] = '#36a64f'
        if pretext:
            if user_id:
                data[
                    'pretext'] = "*Hi <@" + user_id + ">! Some of the conferences I managed to find! For further details visit* %s" % \
                                                      app.config['TECH_CONF_URL']
            else:
                data['pretext'] = "*Conferences in database*"
            data['mrkdwn_in'] = ['text', 'pretext']
            pretext = False
        response['attachments'].append(data)

    if len(response['attachments']) == 0:
        if user_id is None:
            return None
        data = {}
        data['color'] = '#e60000'
        data['pretext'] = "*Hi <@" + user_id + ">! Could not able to find any conferences for that region*"
        response['attachments'].append(data)
    return response
