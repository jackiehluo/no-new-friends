import os

SECRET_KEY = os.environ['SECRET_KEY']
SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']
APP_TOKEN = os.environ['APP_TOKEN']

DEBUG = False
BCRYPT_LOG_ROUNDS = 13
WTF_CSRF_ENABLED = True
DEBUG_TB_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False

import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

MAIL_USERNAME = os.environ['MAIL_USERNAME']
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

MAIL_DEFAULT_SENDER = os.environ['MAIL_USERNAME']

from authomatic.providers import oauth2

CONFIG = {
	'fb': {      
        'class_': oauth2.Facebook,
        'consumer_key': os.environ['FB_CONSUMER_KEY'],
        'consumer_secret': os.environ['FB_CONSUMER_SECRET'],
        'scope': ['public_profile']
        }
}

USERS_PER_PAGE = 10
