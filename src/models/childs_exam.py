from manage import db

class Childs_Answer(db.Model):
    __tablename__ = 'childs_answer'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer, nullable=False)
    answer_id = db.Column(db.Integer, nullable=True)
    answer_text = db.Column(db.String(), nullable=True)
    score = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return "<Childs Answer: {}, {}, {}>".format(self.child_id, self.answer_id, self.question_id, self.answer_text, self.score)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Childs_Answer.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
