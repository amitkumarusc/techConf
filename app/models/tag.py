from .. import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    channel_id = db.Column(db.Integer, db.ForeignKey('slack_info.id'))

    def __init__(self, name, channel_id):
        self.channel_id = channel_id
        self.name = name

    def save(self):
        db.session.add(self)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self):
        db.session.delete(self)
        return session_commit()

    def __str__(self):
        return 'Tag Name: %s , Channel Id : %s' % (self.name, self.channel_id)


def session_commit():
    try:
        db.session.commit()
    except:
        "error"