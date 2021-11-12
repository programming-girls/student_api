'''
should be able to:
get list of exams
get exam using id
get score
get leaderboard
view other students in class
'''

from flask import Blueprint

from manage import app, db

from src.exam.models.model import Exam, Subject, Question, SubQuestion, Answer, Image, Exams_Done, Student_Answer
from src.users.models.user import User
from src.users.models.user_class import Student, Parent

student = Blueprint('student', __name__)

class Student:
    def __init__(self) -> None:
        pass