import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
csrf = CSRFProtect(app)

