from .. import app
import json
from flask import request
from ..utils.user_choice_handler import parse_user_choice


data = ''


@app.route('/slack/user_response', methods=['POST'])
def user_response():
    global data
    data = json.loads(request.form['payload'])
    return parse_user_choice(data)


@app.route('/slack/user_responsee')
def user_responsee():
    return data