'''
add pupil
see pupil list
see pupil exams
see pupil leaderboard in each class
see pupil leaderboard overrall in class
'''
import os
import requests
from manage import app, db
from flask.json import jsonify
from flask import Blueprint, request, Response
from src.models.user_class import Child, Parent, User

parent = Blueprint('parent', __name__)

parent_keys = ['firstname', 'lastname', 'email', 'password_hash', 'person_type', 'gender']
user_keys = ['firstname', 'lastname', 'gender', 'email', 'password', 'person_type', 'gender', 'yob', 'name_of_physical_School', 'grade']

API_URL = os.environ['API_URL']

def get_token():
    responseObject = dict()
    # get auth
    auth_header = request.headers.get('Authorization')
    if auth_header:
        
            auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None
    print(auth_token, 'hhhhhhhhhhhhhhh')
    if not auth_token:
        responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }

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
    return jsonify(responseObject)

@parent.route('/parent', methods=['GET', 'POST', 'PUT', 'DELETE'])
def parent_():
    
    user = get_token()

    print('user', user)
    
    parent_id = user['id']

    if request.method == 'GET':
        p = Parent.query.filter_by(id=parent_id).first()
        return jsonify(p.serialize())

    data = request.get_json()
    if not data:
        return Response('Invalid Payload',status=400)

    if request.method == 'PUT':
        p = Parent.query.filter_by(id=id).first()
        new_data = request.get_json()
        new_data_keys = new_data.keys()
        for key in new_data_keys:
            if key in user_keys:
                setattr(p, key, new_data[key])  # p.key = new_data[key]
        db.session.commit()
        return jsonify(p.serialize())

    if request.method == 'DELETE':
        p = Parent.query.filter_by(id=id).first()
        db.session.delete(p)
        db.session.commit()
        return jsonify(p.serialize())

@parent.route('/parents_child/<int:parent_id>/<int:child_id>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def my_child(parent_id, child_id=None):
    if request.method == 'POST':
        data = request.get_json()
        res = requests.post(API_URL + '/student/' + str(child_id), data=data)
        return jsonify(res.json())

    if request.method == 'GET':
        s = Child.query.filter_by(parent_id=parent_id).all()
        return jsonify(s.serialize())

    if request.method == 'PUT':
        res = requests.put(API_URL + '/student/' + str(child_id), data=request.get_json())
        return jsonify(res)


    if request.method == 'DELETE':
        res = requests.delete(url=app.config['API_URL'] + '/student/' + child_id)
        return jsonify(res)



