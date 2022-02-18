import os
import json
import pytest
from config import TestingConfig
from src.models.user_auth import User

from app import app, db

app.config.from_object(TestingConfig)
db.drop_all()
db.create_all()
user = User(email='test_user1@email.com', password='ccccckl')
db.session.add(user)
db.session.commit()