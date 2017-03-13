from .. import db


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

    def session_commit(self):
        try:
            db.session.commit()
        except:
            "error"