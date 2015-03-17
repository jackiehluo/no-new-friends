from datetime import datetime
import requests
from urlparse import urlparse
from app import db, bcrypt
from config import APP_TOKEN


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    facebook = db.Column(db.String, unique=True, nullable=True)
    about_me = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, about_me, email, password, confirmed,
                 paid=False, admin=False, confirmed_on=None):
        self.name = name
        self.about_me = about_me
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def has_facebook(self):
        if self.facebook:
            return True
        return False

    def picture(self, width, height):
        img_url = 'https://graph.facebook.com/%s/picture?width=%d&height=%d&redirect=false&access_token=%s' \
                % (self.facebook, width, height, APP_TOKEN)
        r = requests.get(img_url).json()
        return r['data']['url'].encode('utf-8')

    def __repr__(self):
        return '<email {}'.format(self.email)
