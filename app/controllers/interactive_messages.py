from .. import app
from flask import request, Response

data = ''

@app.route('/slack/user_response', methods=['POST'])
def user_response():
    global data
    print "User clicked one button"
    data = request.form['payload']
    return ''


@app.route('/slack/user_responsee')
def user_responsee():
    return data