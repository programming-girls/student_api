import os
import json
import pytest
from config import TestingConfig
from src.models.user_auth import User, BlacklistToken

from app import app, db

app.config.from_object(TestingConfig)
db.drop_all()
db.create_all()
user = User(email='test_user1@email.com', password='ccccckl')
db.session.add(user)
db.session.commit()


@pytest.fixture(autouse=False)
def setup():
    """
    Setup the test environment
    """
    yield
    db.session.remove()
    db.drop_all()


@pytest.mark.parametrize('email, password, expected_status_code', 
                        [
                            ('jomo@gmail.com', 'Jomo@2019', '200 OK'),
                            ('', '', '400 BAD REQUEST'),
                            ('jomo@gmail.com', 'Jomo@2020', '400 BAD REQUEST'),
                            ('moses@hotmail.com', 'Moses@2019', '200 OK'),
                         ])
def test_register(email, password, expected_status_code):
    """
    Test the /register route
    """
    data = {
        'email': email,
        'password': password,
    }   
    response = app.test_client().post('/register',data=json.dumps(data), content_type='application/json')
    assert response.status == expected_status_code

@pytest.mark.parametrize('email, password, expected_status_code', 
                        [
                            ('jomo@gmail.com', 'Jomo@2019', 201),
                            ('', '', 400),
                            ('jomo@gmail.com', 'Jomo@2020', 400),
                            ('moses@hotmail.com', 'Moses@2019', 201),
                         ])
def test_login(email, password, expected_status_code):
    """
    Test the /login route
    """
    data = {
        'email': email,
        'password': password,
    }   
    response = app.test_client().post('/login',data=json.dumps(data), content_type='application/json')   
    assert response.status_code == expected_status_code


@pytest.mark.parametrize('email, expected_status_code',
                        [
                            ('', 400),
                            ('test_user1@email.com', 200),
                            ('kkk@gmail.com', 400)                       
                     ])
def test_forgot_password(email, expected_status_code):
    """
    Test the /forgot_password route
    """
    data = {
        'email': email,
    }   
    response = app.test_client().post('/forgot_password',data=json.dumps(data), content_type='application/json')
    assert response.status_code == expected_status_code

# @pytest.mark.parametrize('email, expected_status_code',
#                         [
#                             ('', 400),
#                             ('test_user1@email.com', 200),
#                             ('kkk@gmail.com', 400)                       
#                      ])
# def test_reset_password(email, expected_status_code):
#     """
#     Test the /reset_password route
#     """
#     data = {
#         'email': email,
#     }
#     get_token = app.test_client().post('/forgot_password',data=json.dumps(data), content_type='application/json')
#     token = get_token.data
#     response = app.test_client().post('/reset_password/{}'.format(token)) 
#     assert response.status_code == expected_status_code


# @pytest.mark.parametrize('email, password, expected_status_code',
#                         [])
# def test_change_password():
#     """
#     Test the /change_password route
#     """
#     url = 'http://localhost:5000/api/v1/auth/change_password'
#     data = {
#         'password': '',
#         'new_password': '',
#     }   
#     response = requests.post(url, json=data)    
#     assert response.status_code == 400


@pytest.mark.parametrize('email, password, expected_status_code',
                            [
                            ('test_user1@email.com', 'ccccckl', 201),
                        ])
def test_logout(email, password, expected_status_code):
    """
    Test the /logout route
    """
    token = app.test_client().post('/login',data=json.dumps({'email': email, 'password': password}), content_type='application/json')

    assert token.status_code == expected_status_code
    token = token.data
    
    response = app.test_client().post('/logout',data=token, content_type='application/json') 

    assert response.status_code == 200

#TO:DO: Test google and facebook login

# @pytest.mark.parametrize('email, password, expected_status_code',
#                         [])
# def test_google_login(email, password, expected_status_code):
#     """
#     Test the /google_login route
#     """
#     data = {
#         'token': '',
#     }   
#     response = app.test_client().post('/google_login', data=json.dumps(data), content_type='application/json')   
#     assert response.status_code == 400

# @pytest.mark.parametrize('email, password, expected_status_code',
#                         [])
# def test_facebook_login():
#     """
#     Test the /facebook_login route
#     """
#     url = 'http://localhost:5000/api/v1/auth/facebook_login'
#     data = {
#         'token': '',
#     }   
#     response = requests.post(url, json=data)    
#     assert response.status_code == 400

