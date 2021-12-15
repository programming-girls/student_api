import pytest
import requests
import json
from parameterized import parameterized, parameterized_class

@parameterized([
    ('jomo@gmail.com', 'Jomo@2019', 200),
    ('', '', 400),
    ('jomo@gmail.com', 'Jomo@2020', 400),
    ('moses@hotmail.com', 'Moses@2019', 200),
])

def test_register(email, password, expected_status_code):
    """
    Test the /register route
    """
    url = 'http://localhost:5000/api/v1/auth/register'
    data = {
        'email': email,
        'password': password,
    }   
    response = requests.post(url, json=data)    
    assert response.status_code == expected_status_code

def test_login():
    """
    Test the /login route
    """
    url = 'http://localhost:5000/api/v1/auth/login'
    data = {
        'email': '',
        'password': '',
    }   
    response = requests.post(url, json=data)    
    assert response.status_code == 400

def test_forgot_password():
    """
    Test the /forgot_password route
    """
    url = 'http://localhost:5000/api/v1/auth/forgot_password'
    data = {
        'email': '',
    }   
    response = requests.post(url, json=data)    
    assert response.status_code == 400

def test_reset_password():
    """
    Test the /reset_password route
    """
    url = 'http://localhost:5000/api/v1/auth/reset_password'
    data = {
        'token': '',
        'password': '',
    }   
    response = requests.post(url, json=data)    
    assert response.status_code == 400

def test_change_password():
    """
    Test the /change_password route
    """
    url = 'http://localhost:5000/api/v1/auth/change_password'
    data = {
        'password': '',
        'new_password': '',
    }   
    response = requests.post(url, json=data)    
    assert response.status_code == 400

def test_logout():
    """
    Test the /logout route
    """
    url = 'http://localhost:5000/api/v1/auth/logout'
    data = {
        'token': '',
    }   
    response = requests.post(url, json=data)    
    assert response.status_code == 400

def test_google_login():
    """
    Test the /google_login route
    """
    url = 'http://localhost:5000/api/v1/auth/google_login'
    data = {
        'token': '',
    }   
    response = requests.post(url, json=data)    
    assert response.status_code == 400

def test_facebook_login():
    """
    Test the /facebook_login route
    """
    url = 'http://localhost:5000/api/v1/auth/facebook_login'
    data = {
        'token': '',
    }   
    response = requests.post(url, json=data)    
    assert response.status_code == 400

