from . import db
from flask_login import UserMixin
from datetime import datetime

profile_interests = db.Table(
    'profile_interests',
    db.Column('profile_id', db.Integer, db.ForeignKey('profile.id'), primary_key=True),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'), primary_key=True)
)

# user_interest = db.Table('user_interest',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'), primary_key=True)
# )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(500))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    age = db.Column(db.Integer)
    emailVerified = db.Column(db.Boolean, default=False)
    sex = db.Column(db.Enum('male', 'female', 'n/o', name='sex'))
    sexualPreference = db.Column(db.Enum('male', 'female', 'everyone', name='sexual_preference'), default='everyone')
    profile = db.relationship("Profile", backref="user", uselist=False)

    reset_token_hash = db.Column(db.String(500), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    def __repr__(self):
        return f"<User {self.username}>"


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to user

    title = db.Column(db.String(150))
    company = db.Column(db.String(150))
    industry = db.Column(db.String(150))
    experienceLevel = db.Column(
        db.Enum('Entry-level', 'Mid-level', 'Senior', 'Manager', 'Director', 'Executive', 'Founder', name='experience_level')
    )
    education = db.Column(db.String(150))
    bio = db.Column(db.String(500))

    # Many-to-many relationship with interests
    interests = db.relationship(
        "Interest",
        secondary=profile_interests,
        backref=db.backref('profiles', lazy='dynamic')
    )
    
    profile_image = db.Column(db.String(300), default='default_profile.png')
    
    image1 = db.Column(db.String(300), default='default1.png')
    image2 = db.Column(db.String(300), default='default2.png')
    image3 = db.Column(db.String(300), default='default3.png')
    image4 = db.Column(db.String(300), default='default4.png')

    verified = db.Column(db.Boolean, default=False)
    online = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(150))
    def __repr__(self):
        return f"<Profile {self.title} of User {self.user_id}>"
    


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Interest {self.name}>"




class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Optional: name of conversation or chat room
    name = db.Column(db.String(150), nullable=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(50), index=True)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)