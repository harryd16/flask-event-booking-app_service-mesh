from flask_sqlalchemy import SQLAlchemy
import datetime

from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    date_created = db.Column(db.DateTime)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the user id to satisfy Flask-Login's requirements."""
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __init__(self, username, password):
        now = datetime.datetime.now()
        self.username = username
        self.password = password
        self.date_created = now

    def __repr__(self):
        return '<User %r>' % self.username

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user = db.relationship('User',
    #    backref=db.backref('users', lazy='dynamic'))
    title = db.Column(db.Text)
    response_going = db.Column(db.Integer)
    response_interested = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    datetime = db.Column(db.DateTime)
    location = db.Column(db.Text)
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer)

    def get_short_description(self):
        return self.description.trim(0,100)

    def tickets_available(self):
        return self.capacity - self.response_going

    def get_description(self):
        return self.description

    def __init__(self, user):
        now = datetime.datetime.now()
        self.user = user
        self.title = title
        self.response_going = 0
        self.response_interested = 0
        self.date_created = now
        self.datetime = None
        self.location = ''
        self.description = ''
        self.capacity = 0

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
        timestamp = datetime.datetime.now()
        guest_tickets = 0

    def __repr__(self):
        return '<Ticket %r>' % self.id
