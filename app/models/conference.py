from flask_mongoalchemy import MongoAlchemy, BaseQuery
import datetime, calendar
from difflib import SequenceMatcher

db = MongoAlchemy()


class Conference(db.Document):
    query_class = BaseQuery
    name = db.StringField()
    start_date = db.DateTimeField()
    end_date = db.DateTimeField()
    location = db.StringField()
    desc = db.StringField()
    url = db.StringField()

    def __str__(self):
        return '%s at %s' % (self.name, self.location)

    @staticmethod
    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = int(sourcedate.year + month / 12)
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    @staticmethod
    def fetch_all_conferences():
        return Conference.query.all()

    @staticmethod
    def fetch_upcoming_conferences(start_date):
        all_conferences = Conference.fetch_all_conferences()
        conferences = []
        for conference in all_conferences:
            if conference.start_date.date() > start_date and conference.start_date.date() < Conference.add_months(start_date, 4):
                conferences.append(conference)
        return conferences

    @staticmethod
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def fetch_from_location(location):
        all_conferences = Conference.fetch_all_conferences()
        conferences = []
        for conference in all_conferences:
            ratio = Conference.similar(location, conference.location.lower())
            if ratio > 0.5:
                conferences.append(conference)

        return conferences
