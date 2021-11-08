from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager


from manage import app, db

from src.exam.models.model import Exam, Subject, Question, SubQuestion, Answers, Image
from src.users.models.user import User

from src.orc_engine.ocr_server import ocr_core, ocr
from src.users.views.user import auth

app.register_blueprint(auth)
app.register_blueprint(ocr)

login_manager = LoginManager()

admin = Admin(app, name='Eshirali School', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Exam, db.session))
admin.add_view(ModelView(Subject, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(SubQuestion, db.session))
admin.add_view(ModelView(Answers, db.session))
admin.add_view(ModelView(Image, db.session))

with app.app_context():
    from src.users.models.user import User
    from src.exam.models.model import Exam, Subject, Question, SubQuestion, Answers, Image

    db.init_app(app)
    db.create_all()
    login_manager.init_app(app)
    login_manager.login_view = "login"

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)