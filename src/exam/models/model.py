from manage import db


Exam_Subject=db.Table('exam_subject',
    db.Column('exam_id', db.Integer, db.ForeignKey('exam.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'))
)


class Exam(db.Model):
    __tablename__ = 'exam'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    year = db.Column(db.String(), nullable=False)
    subject = db.relationship('Subject', secondary=Exam_Subject, backref=db.backref('Exam', lazy='dynamic'),lazy='dynamic')

    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

Subject_Question=db.Table('subject_question',
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
)


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    subject_topic = db.Column(db.String(), nullable=False)
    sub_topic = db.Column(db.String(), nullable=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    question = db.relationship('Question', secondary=Subject_Question, backref=db.backref('Subject', lazy='dynamic'),lazy='dynamic')

    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

Question_Answer=db.Table('question_answer',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id'))
)

Question_Image=db.Table('question_image',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'))
)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    ques = db.Column(db.String(), nullable=False)
    
    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

class SubQuestion(db.Model):
    __tablename__ = 'subquestion'
    id = db.Column(db.Integer, primary_key=True)
    subques = db.Column(db.String(), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def __init__(self):
        super().__init__()
    
    def __repr__(self) -> str:
        return super().__repr__()


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    ans = db.Column(db.String(), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    images_url = db.Column(db.String(), nullable=False)
    question = db.relationship('Question', secondary=Question_Image, backref=db.backref('Image', lazy='dynamic'),lazy='dynamic')

    def __init__(self):
        super().__init__()
    
    def __repr__(self) -> str:
        return super().__repr__()
    
