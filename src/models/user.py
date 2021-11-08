from flask_login import UserMixin
from manage import db
from .model import Exam
from werkzeug.security import generate_password_hash, check_password_hash

User_Exams=db.Table('user_exams',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('exam_id', db.Integer, db.ForeignKey('exam.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    exams = db.relationship('Exam', secondary=User_Exams, backref=db.backref('user', lazy='dynamic'),lazy='dynamic')

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()