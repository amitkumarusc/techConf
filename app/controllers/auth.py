from .. import app
import json
import urllib
import requests
from flask import Flask, render_template, redirect, request, jsonify, Response

CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']

@app.route('/test')
def test():
	return "Heloo"

@app.route('/authsuccess')
def authsuccess():
	temp_code = request.args.get('code')
	token_url = 'https://slack.com/api/oauth.access'
	params = {'client_id' : CLIENT_ID, 'client_secret' : CLIENT_SECRET, 'code' : temp_code}
	token_url = token_url + '?' + urllib.urlencode(params)
	response = requests.get(token_url)
	json_data = json.loads(response.text)
	print "The access token is : ", json_data['access_token']
	return jsonify(json_data)

@app.route('/authslack')
def authslack():
	slack_url = 'https://slack.com/oauth/authorize'
	params = {'client_id' : CLIENT_ID, 'scope' : 'incoming-webhook,commands,bot'}
	slack_url = slack_url + '?' + urllib.urlencode(params)
	print "Making a get request to : ", slack_url 
	return redirect(slack_url)
