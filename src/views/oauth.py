import os
from posix import environ
from flask import redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_login import current_user, login_user
from flask_dance.consumer import oauth_authorized
from src.models.user_auth import User


API_URL = os.environ.get('API_URL')


google_blueprint = make_google_blueprint(
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    scope=["profile", "email"],

)
facebook_blueprint = make_facebook_blueprint(
    client_id=os.environ.get('FACEBOOK_CLIENT_ID'),
    client_secret=os.environ.get('FACEBOOK_CLIENT_SECRET'),
    scope='email'
    )

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    gg_api = '/oauth2/v2/userinfo'

    gg = google.get(gg_api) 
    if gg.ok:
        account_info = gg.json()
        email = account_info['email']

        query = User.query.filter_by(email=email).first()
        try:
            if query is None:
                user = User(email=email)
                user.save()
                login_user(user)
            else:
                login_user(query)
        except Exception as e:
            print(e)
            return redirect(url_for('auth.login'))

@oauth_authorized.connect_via(facebook_blueprint)
def facebook_logged_in(blueprint, token):
    fb_api = 'me?fields=id,email'

    fb = facebook.get(fb_api)
    if fb.ok:
        account_info = fb.json()
        email = account_info['email']

        query = User.query.filter_by(email=email).first()
        try:
            if query is None:
                user = User(email=email)
                user.save()
                login_user(user)
            else:
                login_user(query)
        except Exception as e:
            print(e)
            return redirect(url_for('auth.login'))

