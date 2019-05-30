# UOW Events Webapp
# Harrison Doran / team golfsoftware
# 6 April 2019

# standard python imports
import os
import sys
import datetime
import random

# flask: web framework
# sqlalchemy: sql database
# flask login: manage user login
# Werkzeug: http tools
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_api import status
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.sql.expression import func
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from forms import EditEventForm, upload_image, LoginForm, EventRegistrationForm
from permission import Permission

# init sequence
basedir = os.path.abspath(os.path.dirname(__file__))
random.seed()

UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'data.sqlite')
app.config['SECRET_KEY'] = 'golf0909software' # set different os variable on server
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

# models: database design
from models import *

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_database():
    db.drop_all()
    db.create_all()

title = 'Events @ UOW'

# homepage / event list
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EventRegistrationForm()
    events = Event.query.order_by(Event.event_datetime).all()
    user_events = Event.query.join(Ticket).filter( Ticket.user_id == current_user.get_id() ).order_by(Event.event_datetime)

    if request.method == 'POST':
        try:
            email          = request.form['email']
            quantity       = int(request.form['quantity'])
            event_id       = request.form['event_id']
            event          = Event.query.get(event_id)
            try:
                session_number = int(request.form['session_number'])
            except:
                session_number = 1
            timestamp      = datetime.datetime.now()
            new_ticket = Ticket(
                    user=current_user, event=event,
                    session_number=session_number, timestamp=timestamp,
                    quantity=quantity
            );
            event.response_going += quantity
            db.session.add(new_ticket)
            db.session.commit()
            return redirect( url_for('my_events') )

        except:
            print "failed POST"
            return redirect( url_for('index') )

    return render_template(
            'index.html', navbar_events_active='active', title=title,
            events=events, random=random, user_events=user_events,
            form=form
    )

# deregister event
@app.route('/event/<event_id>/deregister')
@login_required
def deregister(event_id):
    try:
        unwanted_ticket = Ticket.query.filter( (Ticket.user_id == current_user.get_id()) & (Ticket.event_id == event_id)).first()
        associated_event = Event.query.filter( Event.id == unwanted_ticket.event_id ).first()
        # decrement event count by quantity on ticket
        associated_event.response_going -= unwanted_ticket.quantity
        #current_user.events.remove(unwanted_ticket)
        db.session.delete(unwanted_ticket)

        db.session.commit()
        return redirect( url_for('index') )
    except:
        content = {'please move along':'the action attempted in invalid'}
        return render_template("error/401.html"), status.HTTP_401_UNAUTHORIZED

@app.route('/event/<event_id>/delete')
@login_required
def delete_event(event_id):
    unwanted_event = Event.query.get(event_id)
    print(unwanted_event)
    db.session.delete(unwanted_event)
    db.session.commit()
    redirect_( url_for('manage_events') )

# create event page
@app.route('/manage/new_event', methods=['GET', 'POST'])
@login_required # permission also required
def new_event():
    #form = EditEventForm()

    if request.method == 'POST':
        try:
            event_id = int(db.session.query(db.func.max(Event.id)).scalar()) + 1
            title = request.form['title']
            time = request.form['time']
            date = request.form['date']
            event_datetime = datetime.datetime.now()
            location = request.form['location']
            description = request.form['description']
            capacity = int(request.form['capacity'])
            sessions = int(request.form['sessions'])
            price = 0.0
            try:
                price = float(request.form['price'])
            except:
                pass

            new_event = Event( event_id, title, event_datetime, location,
                    description, capacity, current_user, sessions, price )

            db.session.add(new_event)
            db.session.commit()

            discount_code = request.form['discount_code']
            discount_percent = int(request.form['discount_percent'])

            new_discount = Discount( event_id, discount_code, discount_percent )

            db.session.add( new_discount )
            db.session.commit()

            return redirect(url_for('manage_events'))
        except:
            return redirect(url_for('manage_events'))

    return render_template('edit_event.html', navbar_manage_events='active', title="Events @ UOW", event_id=-5)

@app.route('/event/<event_id>/edit')
@login_required
def edit_event(event_id):
    event = Event.query.get(event_id)
    return render_template('edit_event.html', event=event, title=title, navbar_manage_events='active', event_id=event.get_id())


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully.')

        return redirect(url_for('index'))
    return render_template('login.html', form=form, title='Sign In')

# logout procedure
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# event management page
@app.route('/manage/events')
@login_required
def manage_events():
    if current_user.permission == Permission.ADMINISTRATOR:
        manager_events = Event.query.order_by(Event.event_datetime).all()
    else:
        manager_events = Event.query.filter_by(user_creator_id=current_user.get_id()).order_by(Event.event_datetime)
    return render_template(
            'manage_events.html', navbar_manage_events_active='active',
            title=title, manager_events=manager_events, random=random, datetime=datetime
    )

# users' going list
@app.route('/my_events')
@login_required
def my_events():
    #user_events = Event.query.join(User).filter_by(user_id=current_user.get_id())
    user_events = Event.query.join(Ticket).filter( Ticket.user_id == current_user.get_id() ).order_by(Event.event_datetime)
    return render_template(
            'my_events.html', navbar_going_active='active',
            title=title, random=random, datetime=datetime, user_events=user_events
    )

# user management page
@app.route('/manage/user')
@login_required
def manage_users():
    users = User.query.filter_by(permission=1)
    return render_template(
            'manage_users.html',
            navbar_manage_users_active='active', title=title,
            tabs_manage_users_active='active', users=users
    )

# individual user edit
@app.route('/manage/administrator/<username>')
@login_required
def manage_individual_administrator(username):
    return render_template('base.html', title=username)

@app.route('/manage/stats')
@login_required
def manage_stats():
    return render_template('base.html', title=title)

# user management page
@app.route('/manage/event_manager')
@login_required
def manage_event_managers():
    users = User.query.filter_by(permission=2)
    return render_template(
            'manage_users.html',
            navbar_manage_users_active='active', title=title,
            tabs_manage_event_managers_active='active', users=users,
    )

# individual event manager edit
@app.route('/manage/event_manager/<username>')
@login_required
def manage_individual_event_manager(username):
    return render_template('base.html', title=username)

# user management page
@app.route('/manage/administrator')
@login_required
def manage_administrators():
    users = User.query.filter_by(permission=3)
    return render_template(
            'manage_users.html', navbar_manage_users_active='active',
            title=title, tabs_manage_administrators_active='active', users=users
    )

# individual administrator edit
@app.route('/manage/user/<username>')
@login_required
def manage_individual_user(username):
    return render_template('base.html', title=username)

# event search results
@app.route('/?search=<search_term>', methods=['GET'])
def search_results(search_term):
    events = Event.query.filter(Event.title.like('%' + search_term + '%')).order_by(Event.title).all()
    try:
        events = Event.query.filter(Event.title.like('%' + search_term + '%')).order_by(Event.title).all()
        return render_template('index.html', events=events, title=title)
    except:
        return redirect( url_for('index') )

'''
# event calendar
@app.route('/events_calendar')
def events_calendar():
    return render_template('events_calendar.html', navbar_calendar_active='active', title=title)
'''
'''
# event page (includes session registration)
@app.route('/event/<event_id>', methods=['GET', 'POST'])
def event_page(event_id):
    form = EventRegistrationForm()
'''
'''
# event registration
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
    ## on trusted networks you can call flask run --host=0.0.0.0 to allow other users to access
    app.run()

    ## uncomment to clear database
    ## run test_data.py for test data
    #create_database()

