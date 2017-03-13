from .. import db
from base_model import BaseModel

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('channel_id', db.Integer, db.ForeignKey('channel.id'))
                )

twitter_tags = {'ruby': '@rubyconf', 'python': '@pyconindia', 'rails': '@railsconf', 'android': '@droidcon',
                'javascript': '@jsconf', 'go': '@golang'}


class Tag(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    twitter_handle = db.Column(db.String(255))
    channels = db.relationship('Channel', secondary=tags,
                               backref=db.backref('tags', lazy='dynamic'))

    def __init__(self, name):
        self.name = name
        self.twitter_handle = twitter_tags[name.lower()]

    def __str__(self):
        return 'Tag Name: %s , Twitter handle : %s' % (self.name, self.twitter_handle)

    @staticmethod
    def create_tags():
        for tag_name in twitter_tags.keys():
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag is None:
                tag = Tag(tag_name)
                tag.save()