'''
add pupil
see pupil list
see pupil exams
see pupil leaderboard in each class
see pupil leaderboard overrall in class
'''
import os
import requests
from flask import Blueprint, request
from flask.json import jsonify

from manage import app, db

from src.models.user import User
from src.models.user_class import Child, Parent

parent = Blueprint('parent', __name__)
user_keys = ['firstname', 'lastname', 'gender', 'email', 'password', 'person_type', 'gender', 'yob', 'name_of_physical_School', 'grade']
API_URL = os.environ['API_URL']


@parent.route('/parent/<int:parent_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def parent_(self, id=None):
    if request.method == 'POST':
        p = Parent(
            firstname = request.form['firstname'],
            lastname = request.form['lastname'],
            email = request.form['email'],
            password = request.form['password'],
            person_type = 'Parent',
            gender = request.form['gender']
            )
        db.session.add(p)
        db.session.commit()

    if request.method == 'GET':
        p = Parent.query.filter_by(id=id).first()
        return jsonify(p.serialize())

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



