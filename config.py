# This file contains most of the configuration variables that your app needs.
import os
from datetime import timedelta
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    SECRET_KEY = "\xf9'\xe4p(\xa9\x12\x1a!\x94\x8d\x1c\x99l\xc7\xb7e\xc7c\x86\x02MJ\xa0"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost/flask-api'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class HerokuConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost/flask-api'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class AWSConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost/flask-api'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class CircleCiConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost/flask-api'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost/flask-api-test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


config_environments = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}