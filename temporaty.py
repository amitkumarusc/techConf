import requests, json
from datetime import datetime
from ..models.conference import Conference
from notifier import send_to_all_channels, format_conference_data
import psycopg2

def parse_date(raw_date):
	year, month, day = map(int, raw_date.split('-'))
	return datetime(year=year, day=day, month=month)

def fetch_conferences():


	arr = ["""Originally, the tower was built for Expo 70 and housed in the Festival Plaza building known as Big Roof designed by Japanese architect Kenzo Tange. The tip of the tower projected out of the Big Roofs ceiling due to the height of the building. After the completion of the tower projecting through the Big Roof, a Japanese science fiction writer, Sakyo Komatsu, looked at it and said he associated it with a sexual description in a Japanese novel, Season of the Sun, where a character broke through a sliding paper door.[1] The creator of the tower, Taro Okamoto, heard about it, and named the tower as the Tower of the Sun.[2]""",
			"""On October 11 and 12, 2003, the inside of the Tower of the Sun was opened to a selected 1,970 people (the figure was chosen for the year the expo was held). Prior to the opening, over 24,000 people applied for it so the Commemorative Organization for the Japan World Exposition 70 made a decision to open the tower again in November and December in the same year.[3] The event to release the inside irregularly continued, and over 40,000 people[4] in total visited the inside of the tower until October 2006. Due to the repair and renovation for the 40th anniversary event of the Expo 70 in 2010, access to the Towers interior was closed again.[4] After additional repairs it was to be permanently open to the public starting in 2014.[5] As of December, 2015, the Towers interior is not open to the public.[6]""",
			"""Inside of the tower, an artwork called the Tree of Life was exhibited, and many miniatures and objects created by the Tsuburaya Productions were suspended from the tree. It was 45 metres high and represents the strength of the life heading to the future.[8] In the tower, there were moving staircases surrounding the tree and a lift which enabled visitors to go to the upper floor. One of the lifts inside was connected to a part of the Big Roof through the opened wall, which was closed after the expo. Originally, The Tower of Mother and The Tower of Youth were also placed on the east and west area in the expo, both were created by Taro Okamoto, and later they were removed."""]



	print "fetching json"
	url = 'https://talkfunnel.com/json'
	resp = requests.get(url)
	data = resp.json()





	try:
		conn = psycopg2.connect("dbname='template1' user='' host='localhost' password=''")
		cursor = conn.cursor()
	except:
		print "I am unable to connect to the database"






	cnt = 0
	for conference in data['spaces']:
		cnt += 1
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










		user_id = 1
		if cnt > 50:
			user_id = 2

		query =  """INSERT INTO "conferences" ("title", "location", "description",
					"url", "start_date", "end_date", "user_id", "created_at", "updated_at")
					 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
		data = (title, location, arr[cnt%3], url, start_date, end_date, user_id, "017-02-08 12:35:00.150459",
					 "017-02-08 12:35:00.150459")
		cursor.execute(query, data)
		conn.commit()






