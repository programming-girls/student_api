from manage import db
from ...exam.models.model import Exam
import datetime as dt
from datetime import datetime

'''
For many to many relationships: 
a student can do more than one exam
a parent can have more than one student
'''

User_Exams=db.Table('user_exams',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('exam_id', db.Integer, db.ForeignKey('exam.id'))
)

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

    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()


class Student(Person):
    __tablename__ = 'student'
    email_address = db.Column(db.String(255), db.ForeignKey(
                                "person.email_address"))
    student_index = db.Column(db.String(50), unique=True, primary_key=True)
    exams = db.relationship('Exam', secondary=User_Exams, backref=db.backref('student', lazy='dynamic'),lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    __mapper_args__ = {
        "polymorphic_identity": "Student",
    }
    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()


class Parent(Person):
    __tablename__ = 'parent'
    email_address = db.Column(db.String(255), db.ForeignKey(
                                "person.email_address"))
    children = db.relationship('Student', secondary=Parents_Children, backref=db.backref('parent', lazy='dynamic'),lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    __mapper_args__ = {
        "polymorphic_identity": "Parent",
    }
    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()
