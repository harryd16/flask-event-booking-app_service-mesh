# UOW Events Webapp
# Harrison Doran / team golfsoftware
# 6 April 2019

# standard python imports
import os
import datetime

# flask: web framework
from flask import Flask, render_template, request, redirect, url_for
# sqlalchemy: sql database
from flask_sqlalchemy import SQLAlchemy
# flask login: manage user login
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import flask_login
# Werkzeug: http tools
from werkzeug.utils import secure_filename

import random

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'data.sqlite')
app.config['SECRET_KEY'] = 'golf0909software'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

# models: database design
from models import *

from forms import EditEventForm, upload_image

login_manager = LoginManager()
login_manager.init_app(app)

title = 'Events @ UOW'


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_database():
    db.drop_all()
    db.create_all()

random.seed()

# homepage / event list
@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', navbar_events_active='active', title=title, events=events, random=random)

# create event page
@app.route('/new_event', methods=['GET', 'POST'])
# @login_required # permission also required
def new_event():
    form = EditEventForm()

    if request.method == 'POST' and form.validate():
        # do stuff here
        new_event = Event(form.title, form.time, form.date, form.location, form.description, form.capacity, form.image_url)

        # commit
        return redirect(url_for('manage_events'))

    return render_template('edit_event.html', form=form, navbar_manage_events='active')

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return render_template('login.html', form=form, title=title)

# logout procedure
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(somewhere)

# event management page
@app.route('/manage_events')
# @login_required
def manage_events():
    return render_template('manage_events.html', navbar_manage_events_active='active', title=title)

# event search results
@app.route('/search?=<event_search>')
def search_results(search):
    return render_template('search_results.html', event_search=search, title=title)

# event calendar
@app.route('/events_calendar')
def events_calendar():
    return render_template('events_calendar.html', navbar_calendar_active='active', title=title)

# event registration
'''
@app.route('/event/<event_id>/register' methods=['GET', 'POST'])
@login_required
def event_registration(event_id):
    form = EventRegistrationForm()
    if form.validate_on_submit():
        # event.register(user)
        flask.flash('User has registered for event ___')

        next = flask.request.args.get('next')
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return render_template('event_registration.html', form=form)
'''


if __name__ == "__main__":
    app.run()
    #create_database()

