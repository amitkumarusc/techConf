# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
MONGOALCHEMY_DATABASE = 'techConf'
MONGOALCHEMY_CONNECTION_STRING = os.environ.get('MONGO_URL')

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
CLIENT_ID = '133078337040.134000073828'
CLIENT_SECRET = 'af8bf6d0093d033ebe0c6f7953e8da9c'

# Schedule timings
DB_UPDATER_TIME = 20 * 60
NOTIFICATION_TIME = 2 * 60
SUGGEST_TAG_TIME = 1 * 60

# Tweets Timings
# (hours, minutes, seconds)
SEND_SAME_TWEET_TIMER = (0, 1, 0)

# TechConf Url
TECH_CONF_URL = 'https://sheltered-tundra-40581.herokuapp.com/'

#Heroku python app
REDIRECT_URL = 'https://ancient-badlands-14496.herokuapp.com/authsuccess'