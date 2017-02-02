import requests, json
from datetime import datetime
from ..models.conference import Conference
from notifier import send_to_all_channels, format_conference_data

def parse_date(raw_date):
	year, month, day = map(int, raw_date.split('-'))
	return datetime(year=year, day=day, month=month)

def fetch_conferences():
	print "fetching json"
	url = 'https://talkfunnel.com/json'
	resp = requests.get(url)
	data = resp.json()
	for conference in data['spaces']:
		title = conference['title'].strip()
		url = conference['url'].strip()
		start_date = parse_date(conference['start'])
		try:
			end_date = parse_date(conference['end'])
		except:
			end_date = start_date
		try:
			location = str(conference['datelocation']).split(',', 1)[1].strip()
		except:
			location = conference['datelocation']
		count = Conference.query.filter(Conference.name==title).count()
		if count == 0:
			print "Document not present. Inserting"
			mConf = Conference(name=title, start_date=start_date, end_date=end_date, url=url, location=location, desc="")
			mConf.save()
			data = format_conference_data([mConf])
			send_to_all_channels(data)
