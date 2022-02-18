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
from flask_login import login_required, current_user
from src.models.user_auth import User
from src.models.user_class import Child
from src.models.childs_exam import Childs_Answer

child = Blueprint('child', __name__)

user_keys = ['firstname', 'lastname', 'gender','gender', 'yob', 'name_of_physical_School', 'grade']
exam_keys = ['child_id', 'question_id', 'answer_id']
EXAM_API_URL = os.environ['EXAM_API_URL']

def score(ans_id: int, question_id: int, ans_text: str) -> int:
    '''
    Calculate score of answer
    '''
    score = 0

    if not question_id:
        return score

    if ans_id == None and ans_text is None: # if no answer is given either as text or id, then score is 0
        return score

    if ans_id and question_id: # if question and ans_id are given, then call api to get choice answer
        data = {
            'question_id': question_id,
            'student_choice': ans_id
        }
        score = requests.get(EXAM_API_URL + '/cms', data=data)

    if ans_text and question_id: # if question and ans_text are given, then call api to get text answer
        data = {
            'question_id': question_id,
            'student_answer': ans_text
        }
        score = requests.get(EXAM_API_URL + '/tms', data=data)

    return score

@child.route('/child', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def child_view():
    '''
    CRUD for the child profile
    '''
    if current_user.is_authenticated:

        child_id = current_user.id

        if request.method == 'GET':
            '''
            get child profile
            '''
            res = Child.query.filter_by(id=child_id).first()
            return Response(res)

        data = request.get_json()
        if not data:
            return Response('Invalid Payload',status=400)

        if request.method == 'POST':
            '''
            Create a new child
            '''

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

        if request.method == 'PUT':
            '''
            Update child profile
            '''
            s = Child.query.filter_by(id=child_id).first()
            new_data = request.get_json()
            new_data_keys = new_data.keys()
            for key in new_data_keys:
                if key in user_keys:
                    setattr(s, key, new_data[key])
            db.session.commit()
            return Response('Success', status=200)
        
        if request.method == 'DELETE':
            '''
            Delete child profile
            '''
            s = Child.query.filter_by(id=child_id).first()
            db.session.delete(s)
            db.session.commit()

            unittest.assertFalse(Child.query.filter(id=child_id).exists())

            return Response('Success', status=200)
    else:
        return Response('Not Authorized', status=401)

@child.route('/child/exams', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def child_exams(child_id):
    '''
    CRUD for the child exams

    '''

    if current_user.is_authenticated:

        child_id = current_user.id

        if request.method == 'GET':
            res = Childs_Answer.query.filter_by(child_id=child_id).all()
            return Response([i.serialize() for i in res])

        data = request.get_json()
        if not data:
            return Response('Invalid Payload',status=400)

        if request.method == 'POST':
            '''
            child answers an exam question
            '''
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

    else:
        return Response('Not Authorized', status=401)







            
