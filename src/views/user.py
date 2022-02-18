import json
import os
from flask import Blueprint, Response, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user, fresh_login_required, \
    login_required
from app import login_manager


from manage import db, mail
from flask_mail import Message

from src.models.user_auth import User, BlacklistToken
from flask_dance.contrib.facebook import facebook
from flask_dance.contrib.google import google

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
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

    u = User.query.filter(User.email == email).first()

    if u:
        return Response('email already registered', status=400)
    else:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return Response('User registered', status=200)

@auth.route('/login', methods=['POST'])
def login():
    """
    Handle requests to the /login route
    Log an User in through the login form
    """

    # bypass if user is already logged in
    if current_user.is_authenticated:
        pass

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
        return Response('Please check your login details and try again', status=400)
    
    login_user(user, remember=True)

    return Response('You are now logged in',status=201)

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

@auth.route('/change_password', methods=['GET', 'POST'])
def change_password(token):

    data = request.get_json()
    if not data:
        return Response('Invalid payload', status=400)
    
    password = data.get('password')
    new_password = data.get('new_password')

    if not password:
        return Response('password not provided', status=400)
    if not new_password:
        return Response('new_password not provided', status=400)


@auth.route('/reset_password/<token>', methods=['POST'])
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

    return redirect(url_for('auth.login'))

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return Response('logged out', status=200)


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return Response('User not found', status=400)


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return Response('You must be logged in to view that page.', status=401)
    
    
@auth.route('/google_login', methods=['GET', 'POST'])
def google_login():
    url = '/google' if google.authorized else url_for('google.login')
    return redirect(url)

@auth.route('/facebook_login', methods=['GET', 'POST']) 
def facebook_login():
    url = '/facebook' if facebook.authorized else url_for('facebook.login')
    return redirect(url)
