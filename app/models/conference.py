from flask_mongoalchemy import MongoAlchemy, BaseQuery

db = MongoAlchemy()

class Conference(db.Document):
	query_class = BaseQuery
	name = db.StringField()
	date = db.StringField()	#Need to change it to date type
	location = db.StringField()
	desc = db.StringField()
	url = db.StringField()

	def __str__(self):
		return '%s at %s'%(self.name, self.location)

