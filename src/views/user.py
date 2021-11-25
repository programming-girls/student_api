import json
import os
import re
import requests
from flask import Blueprint, Response, redirect, url_for, request
from flask_login import login_required, login_user, logout_user

from manage import db, mail
from flask_mail import Message

from src.models.user import User
from flask_dance.contrib.facebook import facebook
from flask_dance.contrib.google import google

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an Userto the database through the registration form
    """

    data = request.get_json()
    if not data:
        return Response('Invalid Payload', status=400)
    
    email = data.get('email')
    password = data.get('password')

    if not email:
        return Response('email not provided', status=400)
    if not password:
        return Response('password not provided', status=400)
    
    user = User.query.filter_by(email=email).first()
    if user:
        return Response('email already registered', status=400)
    else:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return Response('user added', status=200)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an User in through the login form
    """
    data = request.get_json()

    if not data:
        return Response('Invalid payload', status=400)
    
    email = data.get('email')
    password = data.get('password')

    if not email:
        return Response('email not provided', status=400)
    if not password:
        return Response('password not provided', status=400)

    user = User.query.filter_by(email=email).first()
    if not user:
        return Response('user not found', status=400)

    if not user.verify_password(password):
        return Response('invalid password', status=400)
    login_user(user)
    return Response('user logged in', status=200)

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    data = request.get_json()
    if not data:
        return Response('Invalid payload', status=400)
    
    email = data.get('email')
    if not email:
        return Response('email not provided', status=400)
    user = User.query.filter_by(email=email).first()
    if not user:
        return Response('user not found', status=400)
    token = user.generate_reset_token()

    msg = Message('Password Reset Request', sender=os.environ['MAIL_USERNAME'], recipients = [email])
    msg.body = 'To reset your password, click the following link: {}'.format(url_for('auth.reset_password', token=token, _external=True))
    mail.send(msg)
    return Response('email sent', status=200)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    data = request.get_json()
    if not data:
        return Response('Invalid payload', status=400)
    
    password = data.get('password')

    if not password:
        return Response('password not provided', status=400)
    user = User.verify_reset_token(token)
    if not user:
        return Response('invalid token', status=400)
    user.password = password
    db.session.commit()
    return Response('password reset', status=200)
    
    

@auth.route('/google_login', methods=['GET', 'POST'])
def google_login():
    url = '/google' if google.authorized else url_for('google.login')
    return redirect(url)

@auth.route('/facebook_login', methods=['GET', 'POST']) 
def facebook_login():
    url = '/facebook' if facebook.authorized else url_for('facebook.login')
    return redirect(url)

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    logout_user()
    return Response('You have successfully been logged out.')

