def ask_question(question, tags):
    response = {'text': '*%s*'%question, 'attachments': []}
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
