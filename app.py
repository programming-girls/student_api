from flask_login import LoginManager


from manage import app, db

from src.exam.models.model import Exam, Subject, Question, SubQuestion, Answer, Image, Exams_Done, Student_Answer
from src.users.models.user import User
from src.users.models.user_class import Student, Parent

#blueprints
from src.orc_engine.ocr_server import ocr_core, ocr
from src.users.views.user import auth
from src.exam.views.text_marking_scheme import text_marking_scheme
from src.exam.views.choice_marking_scheme import choice_marking_scheme
from src.users.views.admin_views import ad

#register blueprints
app.register_blueprint(auth)
app.register_blueprint(ocr)
app.register_blueprint(text_marking_scheme)
app.register_blueprint(choice_marking_scheme)
app.register_blueprint(ad)

login_manager = LoginManager()

with app.app_context():
    from src.users.models.user import User
    from src.users.models.user_class import Student, Parent
    from src.exam.models.model import Exam, Subject, Question, SubQuestion, Answer, Image, Exams_Done, Student_Answer

    db.init_app(app)
    db.create_all()
    login_manager.init_app(app)
    login_manager.login_view = "login"

 # Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)