from .. import app
from flask import request, Response
from ..utils.user_choice_handler import parse_user_choice


data = ''


@app.route('/slack/user_response', methods=['POST'])
def user_response():
    global data
    print "User clicked one button"
    data = request.form['payload']
    parse_user_choice(data)
    return ''


@app.route('/slack/user_responsee')
def user_responsee():
    return data