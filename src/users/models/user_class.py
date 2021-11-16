from manage import db
from ...exam.models.model import Exam
import datetime as dt
from datetime import datetime

'''
For many to many relationships: 
a student can do more than one exam
a parent can have more than one student
'''

class Person(db.Model):
    PERSON_TYPES = [
       ('parent', 'Parent'),
       ('student', 'Student')
    ]
    GENDER_TYPES = [
       ('male', 'Male'),
       ('female', 'Female')
    ]
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String, nullable=False)
    LastName =  db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, unique=True, nullable=False)
    person_type = db.Column(db.ChoiceType(PERSON_TYPES),  default='parent')
    gender = db.Column(db.ChoiceType(GENDER_TYPES),  default='female')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    __mapper_args__ = {
        "polymorphic_identity": "person",
        "polymorphic_on": person_type
    }

    def __repr__(self):
        return "<{}: {} {}>".format(self.person_type, self.first_name,
                                    self.last_name)

class Parent(Person):
    __tablename__ = 'parent'
    children = db.relationship('Student', backref=db.backref('parent', lazy='dynamic'),lazy='dynamic')

    __mapper_args__ = {
        "polymorphic_identity": "Parent",
    }

    def __repr__(self):
        return "<Parent ID: {}>".format(self.id)

class Student(Person):
    __tablename__ = 'student'
    CHILD_TYPES = [
       ('pupil', 'Pupil'),
       ('student', 'Student')
    ]
    name_of_physical_school = db.Column(db.String, nullable=True)
    yob = db.Column(db.DateTime, default=datetime.now)
    grade = db.Column(db.String, nullable=True)
    child_type = db.Column(db.ChoiceType(CHILD_TYPES), default='pupil')
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))

    __mapper_args__ = {
        "polymorphic_identity": "Student",
    }

    def __repr__(self):
        return "<Student ID: {}>".format(self.id)

