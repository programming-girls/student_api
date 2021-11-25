'''
should be able to:
deactivate/delete user| Update| list/Get with ID
add parent| delete| Update| list/Get with ID
add student| delete| Update| list/Get with ID
add Exam | delete| Update| list/Get with ID
'''
from flask import Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from manage import app, db

from src.models.user import User
from src.models.user_class import Child, Parent

ad = Blueprint('ad', __name__)


admin = Admin(app, name='Eshirali School', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Child, db.session))
admin.add_view(ModelView(Parent, db.session))
