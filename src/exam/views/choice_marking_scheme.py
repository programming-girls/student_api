from flask import Blueprint,request, jsonify
from manage import app
from src.exam.models.model import Question_Answer, Answer,  Question


choice_marking_scheme = Blueprint('choice_marking_scheme', __name__)

class Choice_marking_scheme:
    def __init__(self, student_choice: str, question_id: int) -> None:
        self.student_choice = student_choice
        self.question_id = question_id

    def get_answer_from_db(self) -> str:
        ans = Answer.query.filter(Answer.question.any(id= self.question_id )).first()
        return ans

    def compare_choice(self) ->bool:

        correct_ans = self.get_answer_from_db()
        if self.student_choice == correct_ans:
            return True
        return False

@choice_marking_scheme.route('/cms', methods=['GET'])
def get_answer():
    data = request.get_json()

    if not data:
        return jsonify({"message": "add data to the body in json format"})

    
    sa = data['student_choice']
    qi = data['question_id']
    cms = Choice_marking_scheme(sa, qi)

    return jsonify({"score": cms.compare_choice()})

if __name__ == '__main__':
    Choice_marking_scheme()