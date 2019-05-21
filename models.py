from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from permission import Permission
from flask_login import UserMixin

from app import db, login

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    pw_hash = db.Column(db.String(120))
    date_created = db.Column(db.DateTime)
    authenticated = db.Column(db.Boolean, default=False)
    permission = db.Column(db.String(13), default=Permission.BASE_LEVEL)

    def get_permission(self):
        return Permission(self.permission)

    def set_permission(self, permission):
        self.permission = permission

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __init__(self, username, password, permission):
        self.username = username
        self.set_password(password)
        self.date_created = datetime.datetime.now()
        self.permission = permission

    def __repr__(self):
        return '<User %r>' % self.username

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('users', lazy='dynamic'))
    title = db.Column(db.Text)
    response_going = db.Column(db.Integer)
    response_interested = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    event_datetime = db.Column(db.DateTime)
    location = db.Column(db.Text)
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer)

    def get_short_description(self):
        return self.description[0:300]

    def get_datetime_string_australian(self):
        return self.event_datetime.strftime("%I:%M%p %A %d/%m/%y")

    def set_response_going(self, response_going):
        self.response_going = response_going

    def set_response_interested(self, response_interested):
        self.response_interested = response_interested

    def tickets_available(self):
        return self.capacity - self.response_going

    def get_description(self):
        return self.description

    def __init__(self, id, title, event_datetime, location, description, capacity):
        #self.user = user
        self.title = title
        self.date_created = datetime.datetime.now()
        self.event_datetime = event_datetime
        self.location = location
        self.description = description
        self.capacity = capacity

    def __repr__(self):
        return '<Event %r>' % self.title

class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    timestamp = db.Column(db.DateTime)
    guest_tickets = db.Column(db.Integer)

    user = db.relationship("User", backref="user")
    event = db.relationship("Event", backref="event")

    def __init__(self, user, event):
        self.user = user
        self.event = event
        self.timestamp = datetime.datetime.now()
        self.guest_tickets = 0

    def __repr__(self):
        return '<Ticket %r>' % self.id
