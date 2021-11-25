from sqlalchemy_utils.functions import foreign_keys
from manage import db
import datetime as dt
from datetime import datetime
from sqlalchemy_utils import ChoiceType, EmailType

'''
For many to many relationships: 
a student can do more than one exam
a parent can have more than one student
'''

class Person(db.Model):
    PERSON_TYPES = [
       (u'parent', u'Parent'),
       (u'student', u'Student'),
       (u'admin', u'Admin'),
    ]
    GENDER_TYPES = [
       (u'male', u'Male'),
       (u'female', u'Female')
    ]

    firstname = db.Column(db.String, nullable=False)
    lastname =  db.Column(db.String, nullable=False)
    email = db.Column(EmailType, unique=True, primary_key=True)
    password_hash = db.Column(db.String, unique=True, nullable=False)
    person_type = db.Column(ChoiceType(PERSON_TYPES),  default='student')
    gender = db.Column(ChoiceType(GENDER_TYPES),  default='female')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    __mapper_args__ = {
        "polymorphic_identity": "person",
        "polymorphic_on": person_type
    }

    def __repr__(self):
        return "<{}: {} {}>".format(self.person_type, self.firstname, self.lastname)

class Parent(Person):
    __tablename__ = 'parent'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EmailType, db.ForeignKey('person.email'))
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

class Child(Person):
    __tablename__ = 'child'
    CHILD_TYPES = [
       (u'pupil', u'Pupil'),
       (u'student', u'Student')
    ]
    email = db.Column(EmailType, db.ForeignKey('person.email'))
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
