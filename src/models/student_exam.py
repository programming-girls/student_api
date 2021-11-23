from manage import db

class Student_Answer(db.Model):
    __tablename__ = 'student_answer'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"))
    question_id = db.Column(db.Integer)
    answer_id = db.Column(db.Integer)
    answer_text = db.Column(db.String(), nullable=True)
    score = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return "<Student Answer: {}, {}, {}>".format(self.student_id, self.answer_id, self.question_id, self.answer_text, self.score)
