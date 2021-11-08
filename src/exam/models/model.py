from manage import db

Exam_Subject=db.Table('exam_subject',
    db.Column('exam_id', db.Integer, db.ForeignKey('exam.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'))
)

Subject_Question=db.Table('subject_question',
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
)

Question_SubQuestion = db.Table('question_subquestion',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
    db.Column('subquestion_id', db.Integer, db.ForeignKey('subquestion.id'))
)

Question_Answer=db.Table('question_answer',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id'))
)

Question_Image=db.Table('question_image',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'))
)

class Exam(db.Model):
    __tablename__ = 'exam'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    year = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return "<Exam ID: {}>".format(self.id)

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    subject_topic = db.Column(db.String(), nullable=False)
    sub_topic = db.Column(db.String(), nullable=True)
    exam = db.relationship('Exam', secondary=Exam_Subject, backref=db.backref('Subject', lazy='dynamic'),lazy='dynamic')

    def __repr__(self):
        return "<Subject ID: {}>".format(self.id)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    ques = db.Column(db.String(), nullable=False)
    subject = db.relationship('Subject', secondary=Subject_Question, backref=db.backref('Question', lazy='dynamic'),lazy='dynamic')

    def __repr__(self):
            return "<Question ID: {}>".format(self.id)

class SubQuestion(db.Model):
    __tablename__ = 'subquestion'
    id = db.Column(db.Integer, primary_key=True)
    subques = db.Column(db.String(), nullable=False)
    question = db.relationship('Question', secondary=Question_SubQuestion, backref=db.backref('SubQuestion', lazy='dynamic'),lazy='dynamic')

    def __repr__(self):
        return "<SubQuestion ID: {}>".format(self.id)

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    ans = db.Column(db.String(), nullable=False)
    question = db.relationship('Question', secondary=Question_Answer, backref=db.backref('Answer', lazy='dynamic'),lazy='dynamic')


    def __repr__(self):
        return "<Answer ID: {}>".format(self.id)

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    images_url = db.Column(db.String(), nullable=False)
    question = db.relationship('Question', secondary=Question_Image, backref=db.backref('Image', lazy='dynamic'),lazy='dynamic')

    def __repr__(self):
        return "<Image ID: {}>".format(self.id)

class Exams_Done(db.Model):
    __tablename__ = 'exams_done'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.String(255), db.ForeignKey("exam.id"), nullable=False)
    student_index = db.Column(db.String(255), db.ForeignKey("student.index"))
    score = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return "<Exams Done: {}, {}, {}, {}>".format(self.exam_id, self.student_index, self.score)


class Student_Answer(db.Model):
    __tablename__ = 'student_answer'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(255), db.ForeignKey("student.id"))
    question_id = db.Column(db.String(255), db.ForeignKey("question.id"))
    answer_id = db.Column(db.String(255), db.ForeignKey("answer.id"))

    def __repr__(self):
        return "<Student Answer: {}, {}, {}>".format(self.student_id, self.answer_id, self.question_id)
