from .. import app
import json, urllib, requests
from flask import Flask, render_template, redirect, request, jsonify, Response

from ..models.slackinfo import SlackInfo

CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']


@app.route('/authsuccess')
def authsuccess():
    temp_code = request.args.get('code')
    token_url = 'https://slack.com/api/oauth.access'
    params = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'code': temp_code}
    token_url = token_url + '?' + urllib.urlencode(params)
    response = requests.get(token_url)
    json_data = json.loads(response.text)
    if json_data['ok'] == False:
        return 'Authentication failed! <a href="/">Go to Home</a>'

    access_token = json_data['access_token']
    bot_access_token = json_data['bot']['bot_access_token']
    bot_user_id = json_data['bot']['bot_user_id']
    channel_name = json_data['incoming_webhook']['channel']
    channel_id = json_data['incoming_webhook']['channel_id']
    incomming_webhook_url = json_data['incoming_webhook']['url']
    team_id = json_data['team_id']
    team_name = json_data['team_name']
    user_id = json_data['user_id']

    slack_info = SlackInfo(access_token=access_token, bot_access_token=bot_access_token, bot_user_id=bot_user_id, \
                           channel_name=channel_name, channel_id=channel_id,
                           incomming_webhook_url=incomming_webhook_url, \
                           team_id=team_id, team_name=team_name, user_id=user_id)
    slack_info.save()

    return redirect('/')
    return jsonify(json_data)


@app.route('/authbegin')
def authbegin():
    slack_url = 'https://slack.com/oauth/authorize'
    params = {'client_id': CLIENT_ID, 'scope': 'incoming-webhook,commands,bot'}
    slack_url = slack_url + '?' + urllib.urlencode(params)
    print "Making a get request to : ", slack_url
    return redirect(slack_url)
