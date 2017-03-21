# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

#'postgresql://localhost/techConf'

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# slack developer keys
CLIENT_ID = os.environ['SLACK_CLIENT_ID']
CLIENT_SECRET = os.environ['SLACK_CLIENT_SECRET']

# Schedule timings
DB_UPDATER_TIME = 20 * 60
NOTIFICATION_TIME = 3 * 60 + 1
SUGGEST_TAG_TIME = 2 * 60 + 1
TWITTER_NOTIFICATION_TIME = 4 * 60
UPCOMING_CONF_DAYS = 90

#New Schedular
NOTIFICATIONS_PER_DAY = 5

# Tweets Timings
# (hours, minutes, seconds)
SEND_SAME_MSG_TIMER = (0, 10, 0)

# TechConf Url
TECH_CONF_URL = 'https://sheltered-tundra-40581.herokuapp.com/'

#Heroku python app
REDIRECT_URL = 'https://ancient-badlands-14496.herokuapp.com/authsuccess'