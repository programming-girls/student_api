from manage import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

class Exam(db.Model):
    __tablename__ = 'Exam'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    year = db.Column(db.String(), nullable=False)
    topic = db.Column(db.String(), nullable=False)
    sub_topic = db.Column(db.String(), nullable=False)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    ques = db.Column(db.String(), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)

class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    ans = db.Column(db.String(), nullable=False)
    question_id = db.relationship('Question', backref='answers', lazy=True)

class Images(db.Model):
    pass


class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'
    id = db.Column(db.Integer, primary_key=True)

User_Exams=db.Table('user_exams',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('exam_id', db.Integer, db.ForeignKey('exam.id'))
)