from flask import Blueprint, Response, request
from manage import db
from ..models.model import Exams_Done, Student_Answer
from ...users.models.user_class import Student

exam_marking = Blueprint('exam_marking', __name__)

class marking_scheme():
    pass