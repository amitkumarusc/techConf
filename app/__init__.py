from flask import Flask, render_template
from flask_mongoalchemy import MongoAlchemy
from models.conference import db, Conference
import time, requests, json

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

from controllers import auth, query
from utils import schedular, dbupdater, notifier
from models.slackinfo import SlackInfo

#Start the schedular
schedular.schedule_tasks()

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
	notifier.notify_all()
	return "Initiated"
