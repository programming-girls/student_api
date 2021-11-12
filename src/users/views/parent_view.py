'''
add pupil
see pupil list
see pupil exams
see pupil leaderboard in each class
see pupil leaderboard overrall in class
'''

from flask import Blueprint, request
from flask.json import jsonify

from manage import app, db

from src.exam.models.model import Exam, Subject, Question, SubQuestion, Answer, Image, Exams_Done, Student_Answer
from src.users.models.user import User
from src.users.models.user_class import Student, Parent

parent = Blueprint('parent', __name__)

@parent.route('/parent')
def parent(self, id=None):
    if request.method == 'POST':
        p = Parent(
            firstname = request.form['firstname'],
            lastname = request.form['lastname'],
            email = request.form['email'],
            password = request.form['password'],
            person_type = False,
            gender = request.form['gender']
            )
        db.session.add(p)
        db.session.commit()

    if request.method == 'GET':
        pass

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass


def add_my_student():
    pass

def get_my_students():
    pass

