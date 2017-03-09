from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

Bootstrap(app)

from controllers import auth, query
from utils import schedular, dbupdater, notifier
from models.slackinfo import SlackInfo
from models.conference import Conference

# Start the schedular
#schedular.schedule_tasks()


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def home():
    return render_template('index.html', title="Home", conferences=Conference.fetch_all_conferences())


@app.route('/test')
def test():
    notifier.send_to_all_channels("sample data")
    return "Initiated"


@app.route('/drop_all')
def drop_all():
    db.reflect()
    db.drop_all()
    return 'All tables dropped! Now go to this link to create all tables <a href="/create_all">Create all tables</a>'


@app.route('/create_all')
def create_all():
    db.create_all()
    return "All table schemas created"


@app.route('/slack_info')
def slack_info():
    return notifier.get_slack_details()