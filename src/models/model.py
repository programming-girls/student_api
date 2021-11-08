from manage import db

class Exam(db.Model):
    __tablename__ = 'exam'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    year = db.Column(db.String(), nullable=False)
    topic = db.Column(db.String(), nullable=False)
    sub_topic = db.Column(db.String(), nullable=False)


    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    ques = db.Column(db.String(), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=True)
    ans = db.relationship('Answers', backref='answers', lazy=True)
    sub_q = db.relationship('SubQuestion', backref='subquestion', lazy=True)

    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

class SubQuestion(db.Model):
    __tablename__ = 'subquestion'
    id = db.Column(db.Integer, primary_key=True)
    subques = db.Column(db.String(), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)

    def __init__(self):
        super().__init__()
    
    def __repr__(self) -> str:
        return super().__repr__()


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    ans = db.Column(db.String(), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)

    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

class Images(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    images_url = db.Column(db.String(), nullable=False)
    question_id = db.relationship('Questions', backref='answers', lazy=True)

    def __init__(self):
        super().__init__()
    
    def __repr__(self) -> str:
        return super().__repr__()
    
