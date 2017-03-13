from .. import db
from flask_sqlalchemy import sqlalchemy


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        return self.session_commit()

    def update(self):
        return self.session_commit()

    def delete(self):
        db.session.delete(self)
        return self.session_commit()

    @staticmethod
    def session_commit():
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            print "Database error: ", str(e)