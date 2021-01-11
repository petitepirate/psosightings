from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length

SPECIES = [("Sperm Whale", "Sperm Whale"), ("Common Dolphin", "Common Dolphin"), ("Fin Whale", "Fin Whale")]

class NewUserForm(FlaskForm):
    """Form for adding users."""

    user_name = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    # image_url = StringField('(Optional) Image URL')

class LoginForm(FlaskForm):
    """Login form."""

    user_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class AddSightingForm(FlaskForm):
    """Form for adding Job History"""

    sighting_num = IntegerField('Sighting Number', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    time = StringField('UTC Time of Sighting', validators=[DataRequired()])
    latitude = StringField('Latitude', validators=[DataRequired()])
    longitude = StringField('Longitude', validators=[DataRequired()])
    species = SelectField(u'Species', choices=SPECIES)
    individuals = IntegerField('Number of Individuals', validators=[DataRequired()])

class EditUserForm(FlaskForm):
    """Edit user form."""
    
    # image_url = StringField('Image URL')
    user_name = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class EditSightingForm(FlaskForm):

    sighting_num = IntegerField('Sighting Number', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    time = StringField('UTC Time of Sighting', validators=[DataRequired()])
    latitude = StringField('Latitude', validators=[DataRequired()])
    longitude = StringField('Longitude', validators=[DataRequired()])
    species = SelectField(u'Species', choices=SPECIES)
    individuals = IntegerField('Number of Individuals', validators=[DataRequired()])





