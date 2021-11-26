from manage import db
import datetime as dt
from datetime import datetime
from sqlalchemy_utils import ChoiceType, EmailType
from sqlalchemy_utils.functions import foreign_keys


'''
For many to many relationships: 
a student can do more than one exam
a parent can have more than one student
'''

class Person(db.Model):

    GENDER_TYPES = [
       (u'male', u'Male'),
       (u'female', u'Female')
    ]
    person_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=True)
    lastname =  db.Column(db.String, nullable=True)
    user_type = db.Column(db.String(50))
    gender = db.Column(ChoiceType(GENDER_TYPES), default='female')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    user = db.relationship('User', backref=db.backref('person', uselist=False), lazy='dynamic')

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type
    }

    def __repr__(self):
        return "<User:{}{}>".format(self.id, self.email)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Person.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Parent(Person):
    __tablename__ = 'parent'

    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
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

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Parent.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Child(Person):
    __tablename__ = 'child'
    CHILD_TYPES = [
       (u'pupil', u'Pupil'),
       (u'student', u'Student')
    ]
    p_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
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

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Child.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


