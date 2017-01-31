from flask_mongoalchemy import MongoAlchemy, BaseQuery

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
		return '%s at %s'%(self.name, self.location)

