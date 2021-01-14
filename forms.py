from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length

SPECIES = [("Unidentifiable Baleen Whale", "Unidentifiable Baleen Whale"),
("Unidentifiable Kogia Whale", "Unidentifiable Kogia Whale"),
("Unidentifiable Beaked Whale", "Unidentifiable Beaked Whale"), 
("Unidentifiable Whale", "Unidentifiable Whale"),
("Unidentifiable Dolphin", "Unidentifiable Dolphin"),
("Unidentifiable Porpoise", "Unidentifiable Porpoise"),
("Unidentifiable Seal", "Unidentifiable Seal"),
("Unidentifiable Cetacean", "Unidentifiable Cetacean"),
("Unidentifiable Shelled Sea Turtle", "Unidentifiable Shelled Sea Turtle"),
("Green Sea Turtle", "Green Sea Turtle"),
("Hawksbill Sea Turtle", "Hawksbill Sea Turtle"),
("Kemp's Ridley Sea Turtle", "Kemp's Ridley Sea Turtle"),
("Leatherback Sea Turtle", "Leatherback Sea Turtle"),
("Loggerhead Sea Turtle", "Loggerhead Sea Turtle"),
("Olive Ridley Sea Turtle", "Olive Ridley Sea Turtle"),
("North Atlantic Right Whale", "North Atlantic Right Whale"),
("Bryde's Whale", "Bryde's Whale"),
("Fin Whale", "Fin Whale"),
("Pygmy Fin Whale", "Pygmy Fin Whale"),
("Humpback Whale", "Humpback Whale"),
("Common Minke Whale", "Common Minke Whale"),
("Sei Whale", "Sei Whale"),
("Sperm Whale", "Sperm Whale"),
("Pygmy Sperm Whale", "Pygmy Sperm Whale"),
("Dwarf Sperm Whale", "Dwarf Sperm Whale"),
("Northern Bottlenose Whale", "Northern Bottlenose Whale"),
("Bryde's Beaked Whale", "Bryde's Beaked Whale"),
("Atlantic Spotted Dolphin", "Atlantic Spotted Dolphin"),
("Common Bottlenose Dolphin", "Common Bottlenose Dolphin"),
("Commerson's Dolphin", "Commerson's Dolphin"),
("Common Dolphin", "Common Dolphin"),
("Long-beaked Common Dolphin", "Long-beaked Common Dolphin"),
("Clymene Dolphin", "Clymene Dolphin"),
("Dusky Dolphin", "Dusky Dolphin"),
("Fraser's Dolphin", "Fraser's Dolphin"),
("Guiana Dolphin", "Guiana Dolphin"),
("Heaviside's Dolphin", "Heaviside's Dolphin"),
("Hector's Dolphin", "Hector's Dolphin"),
("Atlantic Humpback Dolphin", "Atlantic Humpback Dolphin"),
("Peale's Dolphin", "Peale's Dolphin"),
("Pantropical Spotted Dolphin", "Pantropical Spotted Dolphin"),
("Northern Right-whale Dolphin", "Northern Right-whale Dolphin"),
("Risso's Dolphin", "Risso's Dolphin"),
("Rough-toothed Dolphin", "Rough-toothed Dolphin"),
("Spinner Dolphin", "Spinner Dolphin"),
("Stripped Dolphin", "Stripped Dolphin"),
("White-beaked Dolphin", "White-beaked Dolphin")]

# ("Atlantic White-sided Dolphin", 
# ("Melon-headed Whale", 
# ("Killer Whale", 
# ("False Killer Whale", 
# ("Pygmy Killer Whale", 
# ("Short-finned Pilot Whale", 
# ("Long-finned Pilot Whale", 
# ("Unidentifiable Pilot Whale", 
# ("Harbor Porpoise", 
# ("Dall's Porpoise", 
# ("Northern Fur Seal", 
# ("Gray Seal", 
# ("Harbor Seal", 
# ("Harp Seal", 
# ("Hooded Seal", 
# ("Ringed Seal", 


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





