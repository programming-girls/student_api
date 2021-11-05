from manage import db

User_Exams=db.Table('user_exams',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('exam_id', db.Integer, db.ForeignKey('exam.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    exams = db.relationship('exam', secondary=User_Exams, backref=db.backref('user', lazy='dynamic'),lazy='dynamic')

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

class Exam(db.Model):
    __tablename__ = 'Exam'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    year = db.Column(db.String(), nullable=False)
    topic = db.Column(db.String(), nullable=False)
    sub_topic = db.Column(db.String(), nullable=False)

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    ques = db.Column(db.String(), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    ans = db.relationship('Answer', backref='answers', lazy=True)

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    ans = db.Column(db.String(), nullable=False)
    question_id = db.relationship('Question', backref='answers', lazy=True)

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

class Images(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    images_url = db.Column(db.String(), nullable=False)
    question_id = db.relationship('Question', backref='answers', lazy=True)

    def __init__(self) -> None:
        super().__init__()
    
    def __repr__(self) -> str:
        return super().__repr__()
    
