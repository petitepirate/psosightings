from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    sightings = db.relationship('Sighting')
    
    @classmethod
    def signup(cls, user_name, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            user_name=user_name,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, user_name, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(user_name=user_name).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Sighting(db.Model):
        
    __tablename__ = 'sightings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sighting_num = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Text, nullable=False)
    longitude = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    individuals = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,
        db.ForeignKey('users.id',  ondelete='cascade')
    )

    user = db.relationship('User')
