from .. import db
from base_model import BaseModel
from ..utils.utils import calculate_hash


class Message(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    text_hash = db.Column(db.String(255))
    last_sent_on = db.Column(db.DateTime())
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))

    def __init__(self, text_msg, last_sent_on, channel_id):
        self.channel_id = channel_id
        self.last_sent_on = last_sent_on
        self.text_hash = calculate_hash(text_msg)

    def __str__(self):
        return 'Hash : %s , Last Sent : %s' % (self.text_hash, self.last_sent_on)
