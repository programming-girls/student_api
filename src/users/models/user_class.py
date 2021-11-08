from manage import db
from ...exam.models.model import Exam
import datetime as dt
from datetime import datetime

'''
For many to many relationships: 
a student can do more than one exam
a parent can have more than one student
'''

Parents_Children=db.Table('parents_children',
    db.Column('parent_id', db.Integer, db.ForeignKey('parent.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'))
)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String, unique=True, nullable=False)
    LastName =  db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, unique=True, nullable=False)
    person_type = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        "polymorphic_identity": "person",
        "polymorphic_on": person_type
    }

    def __repr__(self):
        return "<{}: {} {}>".format(self.person_type, self.first_name,
                                    self.last_name)

class Student(Person):
    __tablename__ = 'student'
    email_address = db.Column(db.String(255), db.ForeignKey(
                                "person.email"))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    __mapper_args__ = {
        "polymorphic_identity": "Student",
    }

    def __repr__(self):
        return "<Student ID: {}>".format(self.id)

class Parent(Person):
    __tablename__ = 'parent'
    children = db.relationship('Student', secondary=Parents_Children, backref=db.backref('parent', lazy='dynamic'),lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    __mapper_args__ = {
        "polymorphic_identity": "Parent",
    }

    def __repr__(self):
        return "<Parent ID: {}>".format(self.id)