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
from flask.wrappers import Response
import requests

from manage import app, db
# from src import login_required

from src.models.user_auth import User
from src.models.user_class import Child
from src.models.childs_exam import Childs_Answer

child = Blueprint('child', __name__)

user_keys = ['firstname', 'lastname', 'gender','gender', 'yob', 'name_of_physical_School', 'grade']
exam_keys = ['child_id', 'question_id', 'answer_id']
API_URL = os.environ['API_URL']

def get_token():
    # get auth
    auth_header = request.headers.get('Authorization')
    if auth_header:
            auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None
    if not auth_token:
        return False

    resp = User.decode_auth_token(auth_token)

    if not isinstance(resp, str):
        user = User.query.filter_by(id=resp).first()
        responseObject = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'email': user.email,
                }
            }
        return user.id

# @login_required
@child.route('/child', methods=['GET', 'POST', 'PUT', 'DELETE'])
def child_view():
    '''
    CRUD for the child profile
    '''
    data = request.get_json()
    if not data:
        return Response('Invalid Payload',status=400)

    child_id = get_token()
    
    
    if request.method == 'POST':

        first_name = data['firstname']
        last_name = data['lastname']
        gender = data['gender']
        yob = data['YOB']
        name_of_physical_School = data['NOPS']
        grade = data['class']
        parent_id = data['parent_id']
        
        c = Child(
            firstname = first_name,
            lastname = last_name,
            gender = gender,
            yob = yob,
            name_of_physical_School = name_of_physical_School,
            grade = grade,
            parent_id = parent_id,
            user_id = child_id
        )
        Child.save(c)
        return Response('Success', status=201)


    if request.method == 'GET':
        res = Child.query.filter_by(id=child_id).first()
        return Response(res)

    if request.method == 'PUT':
        s = Child.query.filter_by(id=child_id).first()
        new_data = request.get_json()
        new_data_keys = new_data.keys()
        for key in new_data_keys:
            if key in user_keys:
                setattr(s, key, new_data[key])
        db.session.commit()
        return Response('Success', status=200)
    
    if request.method == 'DELETE':
        s = Child.query.filter_by(id=child_id).first()
        db.session.delete(s)
        db.session.commit()

        unittest.assertFalse(Child.query.filter(id=child_id).exists())

        return Response('Success', status=200)

# @login_required
@child.route('/child/<int:child_id>/exams', methods=['GET', 'POST', 'PUT', 'DELETE'])
def child_exams(child_id):
    '''
    CRUD for the child exams

    '''
    if request.method == 'GET':
        res = Childs_Answer.query.filter_by(child_id=child_id).all()
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

            correct_answer = 'Answer.query.filter_by(question_id=question_id).filter_by(ans_text).first()'
            question_score = 'Question.query.filter_by(id=question_id).filter_by(score).first()'

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

        a = Childs_Answer(
            child_id = child_id,
            question_id = request.form['question_id'],
            answer_id = request.form['answer_id'],
            answer_text = request.form['answer_text'],
            score = score(request.form['answer_id'] , request.form['question_id'], request.form['answer_text'])
        )
        Childs_Answer.save(a)
        return Response('Success', status=201)
        
    if request.method == 'PUT':
        res = request.get_json()

        a = Childs_Answer.query.filter_by(child_id=child_id, question_id=res['question_id']).first()

        if a:
            new_data = request.get_json()
            new_data_keys = new_data.keys()
            for key in new_data_keys:
                if key in exam_keys:
                    setattr(a, key, new_data[key])
            Childs_Answer.save(a)
            return Response('Success', status=200)
        return Response('No such question', status=404)
        
    if request.method == 'DELETE':

        res = request.get_json()

        a = Childs_Answer.query.filter_by(child_id=child_id, question_id=res['question_id']).first()
        Childs_Answer.delete(a)
        return Response('Success', status=200)







        
