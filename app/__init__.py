from flask import Flask, render_template
from flask_mongoalchemy import MongoAlchemy
from models.conference import db, Conference
import time, requests, json

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

from controllers import auth, query
from utils import schedular, dbupdater

def send_notifications(name):
	url = 'https://hooks.slack.com/services/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'
	headers = {'content-type': 'application/json'}
	data = {'text' : "Time in my clock is :" + time.strftime('%X %x %Z')}
	print name, time.strftime('%X %x %Z')
	
	dbupdater.fetch_conferences()

	#resp = requests.post(url, headers=headers, data=json.dumps(data))
	if False:#resp.status_code != 200:
		print "Something went wrong! Unable to send notifications to slack"


#notification_schedule = schedular.Schedular(3, send_notifications, "Amit Kumar")
#print notification_schedule



@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

@app.route('/')
def home():
	return render_template('index.html')

	conference = Conference.query.first_or_404()
	print dir(conference)
	print "Conference is : ",str(conference)
	return "Success"

@app.route('/save')
def save():
	conference = Conference(name="Ruby Conf", date="12 Jan 2017", location="Bangalore", desc="", url="")
	conference.save()
	return "Success"

@app.route('/test')
def test():
	send_notifications('Amit')
	return "Initiated"
