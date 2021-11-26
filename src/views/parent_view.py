'''
add pupil
see pupil list
see pupil exams
see pupil leaderboard in each class
see pupil leaderboard overrall in class
'''
import os
import json
import random
import requests
from manage import app, db
from flask.json import jsonify
from src import login_required
from flask import Blueprint, request, Response
from src.models.user_class import Child, Parent
from src.models.user_auth import User

parent = Blueprint('parent', __name__)

parent_keys = ['firstname', 'lastname','gender']
child_keys = ['firstname', 'lastname', 'gender','gender', 'yob', 'name_of_physical_School', 'grade']

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

@login_required
@parent.route('/parent', methods=['GET', 'POST', 'PUT', 'DELETE'])
def parent_():
    
    user = get_token() #returns user id

    if user is False:
        return Response(
            mimetype="application/json",
            response=json.dumps({"error": "Invalid token"}),
            status=401
        )
    
    if request.method == 'GET':
        p = Parent.query.filter_by(id=user).first()
        return Response(p)

    data = request.get_json()
    if not data:
        return Response('Invalid Payload',status=400)
    
    if request.method == 'POST':
        
        first_name = data['firstname']
        last_name = data['lastname']
        gender = data['gender']

        p = Parent(
                firstname = first_name, 
                lastname = last_name, 
                gender = gender,
                id = "P" + str(random.randint(1, 999))
                )
        db.session.add(p)
        db.session.commit()
        return Response('success', status=201)


    if request.method == 'PUT':
        p = Parent.query.filter_by(id=id).first()
        new_data = request.get_json()
        new_data_keys = new_data.keys()
        for key in new_data_keys:
            if key in child_keys:
                setattr(p, key, new_data[key])  # p.key = new_data[key]
        db.session.commit()
        return Response('success', status=200)

    if request.method == 'DELETE':
        p = Parent.query.filter_by(id=id).first()
        db.session.delete(p)
        db.session.commit()
        return Response('Delete success', status=200)

@login_required
@parent.route('/parents_child/<int:parent_id>/<int:child_id>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def my_child(parent_id, child_id=None):
    user = get_token() #returns user id

    if user is False:
        return Response(
            mimetype="application/json",
            response=json.dumps({"error": "Invalid token"}),
            status=401
        )
        
    if request.method == 'POST':
        data = request.get_json()
        res = requests.post(API_URL + '/child', data=data)
        return Response(res.text, status=res.status_code)

    if request.method == 'GET':
        s = Child.query.filter_by(parent_id=parent_id).all()
        return Response(s)

    if request.method == 'PUT':
        res = requests.put(API_URL + '/child/' + str(child_id), data=request.get_json())
        return Response(res.json())


    if request.method == 'DELETE':
        res = requests.delete(url=app.config['API_URL'] + '/child/' + child_id)
        return Response(res.json())


