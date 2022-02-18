# This file contains most of the configuration variables that your app needs.
import os
from datetime import timedelta
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_APP = 'app.py'
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_ADMIN_SWATCH = 'cerulean'

    # gmail configuration
    MAIL_SERVER = os.environ['DEVELOP_MAIL_SERVER']
    MAIL_PORT = os.environ['DEVELOP_MAIL_PORT']
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ['DEVELOP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['DEVELOP_MAIL_PASSWORD']

    #google login configuration
    GOOGLE_LOGIN_CLIENT_ID = os.environ['GOOGLE_LOGIN_CLIENT_ID']
    GOOGLE_LOGIN_CLIENT_SECRET = os.environ['GOOGLE_LOGIN_CLIENT_SECRET']
    GOOGLE_LOGIN_AUTH_URI = os.environ['GOOGLE_LOGIN_AUTH_URI']
    GOOGLE_LOGIN_TOKEN_URI = os.environ['GOOGLE_LOGIN_TOKEN_URI']
    GOOGLE_AUTH_PROVIDER_X509_CERT_URL = os.environ['GOOGLE_AUTH_PROVIDER_X509_CERT_URL']

    #facebook login configuration
    FACEBOOK_OAUTH_CLIENT_ID = os.environ['FACEBOOK_OAUTH_CLIENT_ID']
    FACEBOOK_OAUTH_CLIENT_SECRET = os.environ['FACEBOOK_OAUTH_CLIENT_SECRET']

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = os.environ.get('COMPRESSOR_DEBUG')

class HerokuConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_POSTGRESQL_JADE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DockerConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DOCKER_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class AWSConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('AWS_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class CircleCiConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('CIRCLE_CI_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = os.environ['MAIL_PORT']
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') 
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MAIL_SERVER = os.environ['TEST_MAIL_SERVER']
    MAIL_PORT = os.environ['TEST_MAIL_PORT']
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ['TEST_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['TEST_MAIL_PASSWORD']


config_environments = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
    'heroku': HerokuConfig,
    'docker': DockerConfig,
    'aws': AWSConfig,
    'circleci': CircleCiConfig
}