from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length

SPECIES = [("Lead PAM", "Lead PAM"), ("Lead PSO", "Lead PSO"), ("Lead PSO/PAM", "Lead PSO & PAM Dual Role")]

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

    sighting_num = SelectField('Sighting Number', validators=[DataRequired()])
    date = SelectField('Date', validators=[DataRequired()])
    time = IntegerField('UTC Time of Sighting', validators=[DataRequired()])
    latitude = StringField('Latitude', validators=[DataRequired()])
    longitude = StringField('Longitude', validators=[DataRequired()])
    species = StringField(u'Species', choices=SPECIES)
    individuals = StringField('Number of Individuals', validators=[DataRequired()])

class EditUserForm(FlaskForm):
    """Edit user form."""
    
    # image_url = StringField('Image URL')
    user_name = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class EditSightingForm(FlaskForm):

    sighting_num = SelectField('Sighting Number', validators=[DataRequired()])
    date = SelectField('Date', validators=[DataRequired()])
    time = IntegerField('UTC Time of Sighting', validators=[DataRequired()])
    latitude = StringField('Latitude', validators=[DataRequired()])
    longitude = StringField('Longitude', validators=[DataRequired()])
    species = StringField(u'Species', choices=SPECIES)
    individuals = StringField('Number of Individuals', validators=[DataRequired()])





