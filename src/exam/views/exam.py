from flask import Blueprint, Response, request
from manage import db
from ..models.model import Exam, Questions, Answers, Images

exam = Blueprint('exam', __name__)

@exam.route('/title', methods=['GET', 'POST'])
def _Exam(id):
    if request.method == 'POST':
        title = request.form['title'] 
        year = request.form['year'] 
        topic = request.form['topic'] 
        sub_topic = request.form['sub_topic'] 
        exam = Exam(title = title, yeat = year, topic = topic, sub_topic = sub_topic)
        db.session.add(exam)
        db.session.commit()
        return Response('Exam title created sucesfully')

    if request.method == 'GET':
        if not id:
            res = Exam.query.all()
        res = Exam.query.get(id)

        return Response(res)

@exam.route('/questions', methods=['GET', 'POST'])
def _Images(id):
    if request.method == 'POST':
        url = request.form['image_url'] 
        question_id = request.form['question_id'] 
        image = Images(url=url, question_id=question_id)
        db.session.add(image)
        db.session.commit()
        return Response('Image created sucesfully')
    if request.method == 'GET':
        if not id:
            res = Images.query.all()
        res = Images.query.get(id)
        return Response(res)

    

@exam.route('/questions', methods=['GET', 'POST'])
def _Questions(id):
    if request.method == 'POST':
        ques = request.form['question'] 

        exam_id = request.form['exam_id'] 

        image_id = request.form['image_id'] 
        ques = Questions(ques=ques, exam_id=exam_id, image_id=image_id)
        db.session.add(ques)
        db.session.commit()
        return Response('Question created sucesfully')

    if request.method == 'GET':
        if not id:
            res = Questions.query.all()
        res = Questions.query.get(id)
        return Response(res)


@exam.route('/questions', methods=['GET', 'POST'])
def _Answer(id):
    if request.method == 'POST':
        ans = request.form['answer'] 
        question_id = request.form['question_id'] 
        ans = Answers(ans=ans, question_id=question_id)
        db.session.add(ans)
        db.session.commit()
        return Response('Answer created sucesfully')
    if request.method == 'GET':
        if not id:
            res = Answers.query.all()
        res = Answers.query.get(id)
        return Response(res)
    


