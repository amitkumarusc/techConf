from .. import db
from base_model import BaseModel


class Channel(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(512))
    bot_access_token = db.Column(db.String(512))
    bot_user_id = db.Column(db.String(255))
    channel_name = db.Column(db.String(255))
    channel_id = db.Column(db.String(255))
    incoming_webhook_url = db.Column(db.String(1024))
    team_id = db.Column(db.String(255))
    team_name = db.Column(db.String(255))
    user_id = db.Column(db.String(255))
    text_hash = db.Column(db.String(255))
    last_sent_on = db.Column(db.DateTime())
    messages = db.relationship('Message', backref="channel", cascade="all, delete-orphan", lazy='dynamic')

    def __init__(self, access_token, bot_access_token, bot_user_id, channel_name, channel_id,
                 incoming_webhook_url, team_id, team_name, user_id, text_hash, last_sent_on):
        self.access_token = access_token
        self.bot_access_token = bot_access_token
        self.bot_user_id = bot_user_id
        self.channel_name = channel_name
        self.channel_id = channel_id
        self.incoming_webhook_url = incoming_webhook_url
        self.team_id = team_id
        self.team_name = team_name
        self.user_id = user_id
        self.text_hash = text_hash
        self.last_sent_on = last_sent_on

    def __str__(self):
        return "%s %s %s %s %s %s %s %s %s " % (
            self.access_token, self.bot_access_token, self.bot_user_id, self.channel_name, self.channel_id,
            self.incoming_webhook_url, self.team_id, self.team_name, self.user_id)
