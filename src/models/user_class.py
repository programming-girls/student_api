import jwt
from manage import db, app
import datetime as dt
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy_utils import ChoiceType, EmailType
from sqlalchemy_utils.functions import foreign_keys
from werkzeug.security import generate_password_hash, check_password_hash


'''
For many to many relationships: 
a student can do more than one exam
a parent can have more than one student
'''

class User(UserMixin, db.Model):

    __tablename__ = 'user'

    USER_TYPES = [
       (u'parent', u'Parent'),
       (u'student', u'Student'),
       (u'admin', u'Admin'),
    ]
    GENDER_TYPES = [
       (u'male', u'Male'),
       (u'female', u'Female')
    ]

    firstname = db.Column(db.String, nullable=True)
    lastname =  db.Column(db.String, nullable=True)
    email = db.Column(EmailType, unique=True, primary_key=True)
    password_hash = db.Column(db.String, nullable=False)
    user_type = db.Column(ChoiceType(USER_TYPES),  default='student')
    gender = db.Column(ChoiceType(GENDER_TYPES),  default='female')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type
    }
    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, user_id):
        """Generates the auth token and returns it
        """
        try:
            payload = {
                "exp": dt.datetime.now() + dt.timedelta(
                    days=0, seconds=180000),
                "iat": dt.datetime.now(),
                "sub": user_id
            }
            return jwt.encode(
                payload,
                app.config.get("SECRET_KEY"),
                algorithm="HS256"
            )
        except Exception as e:
            return e

    def generate_reset_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': dt.datetime.utcnow() + dt.timedelta(seconds=expires_in)},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    def verify_reset_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token
        """
        try:
            payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"),
                                 options={'verify_iat': False})
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."


    def __repr__(self):
        return "<{}: {}{}>".format(self.user_type, self.firstname, self.lastname)


class Parent(User):
    __tablename__ = 'parent'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EmailType, db.ForeignKey('user.email'))
    children = db.relationship(
        'Child', 
        backref='a_parent',
        lazy='dynamic', 
        primaryjoin="Parent.id == Child.parent_id"
        )

    __mapper_args__ = {
        "polymorphic_identity": "parent",
    }

    def __repr__(self):
        return "<Parent ID: {}>".format(self.id)

class Child(User):
    __tablename__ = 'child'
    CHILD_TYPES = [
       (u'pupil', u'Pupil'),
       (u'student', u'Student')
    ]
    email = db.Column(EmailType, db.ForeignKey('user.email'))
    id = db.Column(db.Integer, primary_key=True)
    name_of_physical_school = db.Column(db.String, nullable=True)
    yob = db.Column(db.DateTime, default=datetime.now)
    grade = db.Column(db.String, nullable=True)
    child_type = db.Column(ChoiceType(CHILD_TYPES), default='pupil')
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    parent = db.relationship(
        'Parent', 
        foreign_keys=[parent_id], 
        backref='child', 
        lazy='joined')

    __mapper_args__ = {
        "polymorphic_identity": "child",
    }

    def __repr__(self):
        return "<Child ID: {}>".format(self.id)

