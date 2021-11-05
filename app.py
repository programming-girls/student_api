from flask import Response
from manage import app, db
from src.model import User, Exam, Questions, Answers, Images

with app.app_context():
    from src.model import User, Exam, Questions, Answers, Images
    db.init_app(app)
    db.create_all()


@app.route('/')
def hello():
    response = Response(status=200)
    return response

if __name__ == '__main__':
    app.run(debug=True)