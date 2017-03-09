def ask_question(question):
    response = {'text': question, 'attachments': []}
    data = {}
    data['pretext'] = '*Basic command to use this app are listed below*'
    data['mrkdwn_in'] = ['text', 'pretext']
    data['title'] = 'Fetch conferences in a region/city'

    data['text'] = 'Choose other technologies you are interested in'\
    data['fallback'] = 'You are unable to subscribe for a technology'
    data['callback_id'] = 'tech_subs'
    data['color'] = '#3AA3E3'
    data['attachment_type'] = 'default'

    button_ruby = {}
    button_ruby['name'] = 'technology'
    button_ruby['text'] = 'Ruby'
    button_ruby['type'] = 'button'
    button_ruby['value'] = 'ruby'

    button_python = {}
    button_python['name'] = 'technology'
    button_python['text'] = 'Python'
    button_python['type'] = 'button'
    button_python['value'] = 'python'

    button_not_interested = {}
    button_not_interested['name'] = 'technology'
    button_not_interested['text'] = 'Not Interested'
    button_not_interested['type'] = 'button'
    button_not_interested['value'] = 'not_interested'
    button_not_interested['confirm'] = { 'title' : 'Are you sure?', 'text' : "Wouldn't you prefer to get technology updates?", 'ok_text' : 'Yes', 'dismiss_text' : 'No'}

    data['actions'] = [button_python, button_ruby, button_not_interested]
    response['attachments'].append(data)

    return response
