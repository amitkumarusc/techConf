from utils import parse_date
import urlparse
import requests
import urllib
from .. import app

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
        print '%s at %s on %s'%(self.name, self.location, self.start_date)

    @staticmethod
    def fetch_all_conferences():
        tech_conf_url = app.config['TECH_CONF_URL'] + 'search.json'
        params = {'query': '', 'search_start_date': '', 'search_end_date': ''}
        tech_conf_url = tech_conf_url + '?' + urllib.urlencode(params)
        conf_data = requests.get(tech_conf_url)
        conferences_json = conf_data.json()
        conferences = []
        for conf in conferences_json:
            conferences.append(Conference(conf))
        return conferences