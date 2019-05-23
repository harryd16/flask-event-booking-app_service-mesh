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
    permission = db.Column(db.Integer, default=Permission.BASE_LEVEL)

    events = db.relationship(
        'Event',
        secondary='ticket'
    )

    def get_permission(self):
        return self.permission

    def set_permission(self, permission):
        self.permission = permission.value

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
    user_creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.Text)
    response_going = db.Column(db.Integer)
    response_interested = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    event_datetime = db.Column(db.DateTime)
    location = db.Column(db.Text)
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer)
    sessions = db.Column(db.Integer)

    users = db.relationship(
        User,
        secondary='ticket'
    )

    def get_short_description(self):
        return self.description[0:300]

    def get_id(self):
        return self.id

    def get_sessions(self):
        return self.sessions

    def get_event_datetime(self):
        return self.event_datetime

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

    def calc_bootstrap_progress(self):
        days_remaining = ( self.event_datetime - datetime.datetime.now() ).days
        if ( days_remaining >= 30 ):
            return 100
        else:
            return round( (float(days_remaining) / 30) * 100 )

    def __init__(self, id, title, event_datetime, location, description, capacity, user, sessions):
        self.user_creator_id = user.get_id()
        self.title = title
        self.date_created = datetime.datetime.now()
        self.event_datetime = event_datetime
        self.location = location
        self.description = description
        self.capacity = capacity
        self.sessions = sessions

    def __repr__(self):
        return '<Event %r>' % self.title

class Ticket(db.Model):
    __tablename__ = 'ticket'

    ticket_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    session_number = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    guest_tickets = db.Column(db.Integer)

    user = db.relationship(User, backref="user_assoc")
    event = db.relationship(Event, backref="event_assoc")

    def __init__(self, user, event, session_number, timestamp, guest_tickets):
        self.user = user
        user_id = user.get_id()
        self.event = event
        event_id = event.get_id()
        self.session_number = session_number
        self.timestamp = datetime.datetime.now()
        self.guest_tickets = 0

    def __repr__(self):
        return '<Ticket %r>' % self.id
