from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

Bootstrap(app)

from controllers import auth, query, interactive_messages
from utils import dbupdater, notifier
from models.channel import Channel
from models.tag import Tag
from models.conference import Conference
import utils.timely.schedular as custom_schedular


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def home():
    return render_template('index.html', title="Home", conferences=Conference.fetch_all_conferences())


@app.route('/test')
def test():
    custom_schedular.start()
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


@app.route('/drop_all_c')
def drop_all_c():
    db.engine.execute("DROP TABLE if exists tags cascade")
    db.engine.execute("DROP TABLE if exists tag cascade")
    db.engine.execute("DROP TABLE if exists message cascade")
    db.engine.execute("DROP TABLE if exists channel cascade")
    return "All table schemas created"


@app.route('/slack_info')
def slack_info():
    return notifier.get_slack_details()

@app.route('/send_temp')
def send_temp():
    notifier.give_tag_suggestion_to_all()
    return 'Suggested tags sent to channels'


if not db.engine.dialect.has_table(db.engine, 'tag'):
    create_all()

Tag.create_tags()

custom_schedular.start()