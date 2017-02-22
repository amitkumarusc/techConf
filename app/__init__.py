from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from models.conference import db, Conference

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
Bootstrap(app)

from controllers import auth, query
from utils import schedular, dbupdater, notifier
from models.slackinfo import SlackInfo

# Start the schedular
schedular.schedule_tasks()


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def home():
    return render_template('index.html', title="Home", conferences=Conference.fetch_all_conferences())


@app.route('/test')
def test():
    notifier.notify_all()
    return "Initiated"
