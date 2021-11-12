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

from src.exam.models.model import Exam, Subject, Question, SubQuestion, Answer, Image, Exams_Done, Student_Answer
from src.users.models.user import User
from src.users.models.user_class import Student, Parent

ad = Blueprint('ad', __name__)


admin = Admin(app, name='Eshirali School', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Exam, db.session))
admin.add_view(ModelView(Subject, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(SubQuestion, db.session))
admin.add_view(ModelView(Answer, db.session))
admin.add_view(ModelView(Image, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Parent, db.session))
admin.add_view(ModelView(Exams_Done, db.session))
admin.add_view(ModelView(Student_Answer, db.session))