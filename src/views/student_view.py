'''
should be able to:
get list of exams done by student
get exam using id
get score of exam
get leaderboard
view other students in class
'''

import os
import unittest
from flask import Blueprint, request, jsonify
import requests

from ...manage import app, db

from src.models.user_class import Student
from src.models.student_exam import Student_Answer

student = Blueprint('student', __name__)

user_keys = ['firstname', 'lastname', 'gender', 'email', 'password', 'person_type', 'gender', 'yob', 'name_of_physical_School', 'grade']
exam_keys = ['student_id', 'question_id', 'answer_id']
API_URL = os.environ['API_URL']

@student.route('/student/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def student_view(student_id=None):
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
            person_type = 'Student',
            gender = request.form['gender'],
            yob = request.form['YOB'],
            name_of_physical_School = request.form['NOPS'],
            grade = request.form['class'],
            parent_id = request.form['parent_id']
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

        unittest.assertFalse(Student.query.filter(id=student_id).exists())

        return jsonify({"message": 'student deleted succesfully'})

@student.route('/student/<int:student_id>/exams', methods=['GET', 'POST', 'PUT', 'DELETE'])
def student_exams(student_id):
    '''
    CRUD for the student exams

    '''
    if request.method == 'GET':
        res = Student_Answer.query.filter_by(student_id=student_id).all()
        return jsonify([i.serialize() for i in res])

    def score(ans_id, question_id, ans_text):
        score = 0
        if ans_id == 0 and ans_text is None:
            score = 0

        if ans_id is None and ans_text is None:
            data = {
                'question_id': question_id,
                'student_choice': ans_id
            }
            score = requests.get(API_URL + '/cms', data=data)

        if ans_text == 0 and ans_id == 0:

            # TO: DO change correct_answer and question_score to API calls

            correct_answer = Answer.query.filter_by(question_id=question_id).filter_by(ans_text).first()
            question_score = Question.query.filter_by(id=question_id).filter_by(score).first()

            data = {
                'student_answer': ans_text,
                'correct_answer': correct_ans_text,
                'question_score': ans_score
            }
            score = requests.get(API_URL + '/tms', data=data)
        return score
        

    if request.method == 'POST':

        correct_ans_text = 'something'
        ans_score = 100

        a = Student_Answer(
            student_id = student_id,
            question_id = request.form['question_id'],
            answer_id = request.form['answer_id'],
            answer_text = request.form['answer_text'],
            score = score(request.form['answer_id'], request.form['question_id'], request.form['answer_text'])
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








        
