from .. import db
from flask_mongoalchemy import BaseQuery


class SlackInfo(db.Document):
    query_class = BaseQuery
    access_token = db.StringField()
    bot_access_token = db.StringField()
    bot_user_id = db.StringField()
    channel_name = db.StringField()
    channel_id = db.StringField()
    incoming_webhook_url = db.StringField()
    team_id = db.StringField()
    team_name = db.StringField()
    user_id = db.StringField()
    text_hash = db.StringField()
    last_sent_on = db.DateTimeField()

    def __str__(self):
        return '%s for team %s' % (self.channel_name, self.team_name)
