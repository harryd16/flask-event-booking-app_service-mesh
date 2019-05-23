from flask_wtf import FlaskForm
from wtforms import Form, StringField, TimeField, DateField, TextAreaField, IntegerField, FileField, PasswordField, SubmitField, BooleanField, validators, DecimalField
from wtforms.fields.html5 import EmailField
# from wtforms.fields import *
# from wtforms.forms import *
# from wtforms.validators import DataRequired

#from models import Event

def upload_image(request):
    form = EditEventForm(request.POST)
    if form.image.data:
        image_data = request_FILES[form.image.name].read()
        open(os.path.join(UPLOAD_FOLDER, form.image.data), 'w').write(image_data)

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')

class EditEventForm(Form):
    title = StringField(u'Title', validators=[validators.input_required()])
    time = TimeField(u'Time', validators=[validators.input_required()])
    date = DateField(u'Date', validators=[validators.input_required()])
    location = StringField(u'Location', validators=[validators.input_required()])
    description = TextAreaField(u'Description')
    capacity = IntegerField(u'Capacity')
    image = FileField(u'Upload Thumbnail Image', [validators.regexp('([/|.|\w|\s|-])*\.(?:jpg|gif|png)')])

    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]','_', field.data)

class EventRegistrationForm(Form):
    session_number = IntegerField('Session number')
    quantity = IntegerField('Number of tickets')
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    register_going = SubmitField('I\'m Going') # bootstrap toggle button


