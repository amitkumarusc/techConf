from utils import parse_date
import urlparse

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