from flask import Blueprint, Response
from flask_login import login_required, login_user, logout_user

from src.forms.user import LoginForm, RegistrationForm
from manage import db
from ..models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an Userto the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        # add User to the database
        db.session.add(user)
        db.session.commit()

    return Response('You have successfully registered! You may now login.')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an User in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # log user in
            login_user(user)

            # redirect to the dashboard page after login
            return Response('login succesful')

        # when login details are incorrect
        else:
            return Response('Invalid email or password.')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    logout_user()
    return Response('You have successfully been logged out.')

