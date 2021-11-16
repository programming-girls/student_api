'''
should be able to:
get list of exams done by student
get exam using id
get score of exam
get leaderboard
view other students in class
'''

from flask import Blueprint, request, jsonify

from ....manage import app, db

from src.exam.models.model import Exam, Subject, Question, SubQuestion, Answer, Image, Exams_Done, Student_Answer
from src.users.models.user import User
from src.users.models.user_class import Student, Parent

student = Blueprint('student', __name__)

user_keys = ['firstname', 'lastname', 'gender', 'email', 'password', 'person_type', 'gender', 'yob', 'name_of_physical_School', 'grade']
exam_keys = ['student_id', 'question_id', 'answer_id']

@student.route('/student/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def student_view(student_id):
    '''
    CRUD for the student profile
    '''
    if request.method == 'GET':
        res = Student.query.filter_by(id=student_id).first()
        return jsonify(res.serialize())

    if request.method == 'POST':
        s = Student(
            firstname = request.form['firstname'],
            lastname = request.form['lastname'],
            email = request.form['email'],
            password = request.form['password'],
            person_type = False,
            gender = request.form['gender'],
            yob = request.form['YOB'],
            name_of_physical_School = request.form['NOPS'],
            grade = request.form['class']
        )
        db.session.add(s)
        db.session.commit()

        return jsonify({"message": 'student added succesfully'})

    if request.method == 'PUT':
        s = Student.query.filter_by(id=student_id).first()
        new_data = request.get_json()
        new_data_keys = new_data.keys()
        for key in new_data_keys:
            if key in user_keys:
                setattr(s, key, new_data[key])
        db.session.commit()
        return jsonify({"message": 'student updated succesfully'})
    
    if request.method == 'DELETE':
        s = Student.query.filter_by(id=student_id).first()
        db.session.delete(s)
        db.session.commit()
        return jsonify({"message": 'student deleted succesfully'})

@student.route('/student/<int:student_id>/exams', methods=['GET', 'POST', 'PUT', 'DELETE'])
def student_exams(student_id):
    '''
    CRUD for the student exams

    '''
    if request.method == 'GET':
        res = Exams_Done.query.filter_by(student_id=student_id).all()
        return jsonify([i.serialize() for i in res])

    if request.method == 'POST':
        a = Student_Answer(
            student_id = student_id,
            question_id = request.form['question_id'],
            answer_id = request.form['answer_id']
        )
        db.session.add(a)
        db.session.commit()

        return jsonify({"message": 'answer added succesfully'})
        
    if request.method == 'PUT':
        a = Student_Answer.query.filter_by(student_id=student_id, question_id=request.form['question_id']).first()
        res = request.get_json()
        res_keys = res.keys()
        for key in res_keys:
            if key in exam_keys:
                setattr(a, key, res[key])
        db.session.commit()
        return jsonify({"message": 'answer updated succesfully'})

    if request.method == 'DELETE':
        a = Student_Answer.query.filter_by(student_id=student_id, question_id=request.form['question_id']).first()
        db.session.delete(a)
        db.session.commit()
        return jsonify({"message": 'answer deleted succesfully'})








        
