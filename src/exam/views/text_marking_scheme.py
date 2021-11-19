from os import abort
from thefuzz import fuzz
from flask import Blueprint,request, jsonify
from manage import app


text_marking_scheme = Blueprint('text_marking_scheme', __name__)

class Text_marking_scheme:
    def __init__(self, student_answer: str, correct_answer: str, question_score: int) -> None:
        self.student_answer = student_answer
        self.correct_answer = correct_answer
        self.question_score = question_score
    

    def compare_answer(self) -> int:
        score = fuzz.partial_token_set_ratio(self.student_answer, self.correct_answer)
        return score

    def get_score(self) ->int:

        res = 0
        fuzz_score = self.compare_answer()
        if fuzz_score <= 50:
            res = 0
        else:
            res = int(fuzz_score * self.question_score) // 100

        return res

@text_marking_scheme.route('/tms', methods=['GET'])
def get_answer():
    data = request.get_json()

    if not data:
        return jsonify({"message": "add data to the body in json format"})

    
    sa = data['student_answer']
    ca = data['correct_answer']
    qs = data['question_score']
    tms = Text_marking_scheme(sa, ca, qs)

    return jsonify({"score": tms.get_score()})

if __name__ == '__main__':
    Text_marking_scheme()