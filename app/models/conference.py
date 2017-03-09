import calendar
import datetime
import urllib
import urlparse

import requests

from .. import app
from ..utils.utils import parse_date


class Conference(object):
    def __init__(self, conf_in_json):
        self.name = conf_in_json['title']
        self.location = conf_in_json['location']
        self.desc = conf_in_json['description']
        self.start_date = parse_date(conf_in_json['start_date'])
        self.end_date = parse_date(conf_in_json['end_date'])
        self.url = conf_in_json['url']
        if not urlparse.urlparse(self.url).scheme:
            self.url = "http://" + conf_in_json['url']

    def __str__(self):
        print '%s at %s on %s' % (self.name, self.location, self.start_date)

    @staticmethod
    def fetch_all_conferences(query='', start_date='', end_date=''):
        tech_conf_url = app.config['TECH_CONF_URL'] + 'search.json'
        params = {'query': query, 'search_start_date': start_date, 'search_end_date': end_date}
        tech_conf_url = tech_conf_url + '?' + urllib.urlencode(params)
        conf_data = requests.get(tech_conf_url)
        conferences_json = conf_data.json()
        conferences = []
        for conf in conferences_json:
            conferences.append(Conference(conf))
        return conferences

    @staticmethod
    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = int(sourcedate.year + month / 12)
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)


    @staticmethod
    def fetch_upcoming_conferences():
        start_date = str(datetime.datetime.now().date())
        end_date = str(Conference.add_months(datetime.datetime.now().date(), 4))
        return Conference.fetch_all_conferences(start_date=start_date, end_date=end_date)
