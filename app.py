from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from manage import app, db

from src.models.model import Exam, Questions,SubQuestion, Answers, Images
from src.models.user import User

from src.views.ocr_server import ocr_core, ocr
from src.views.user import auth

app.register_blueprint(auth)
app.register_blueprint(ocr)

admin = Admin(app, name='Eshirali Primary School', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Exam, db.session))
admin.add_view(ModelView(Questions, db.session))
admin.add_view(ModelView(SubQuestion, db.session))
admin.add_view(ModelView(Answers, db.session))
admin.add_view(ModelView(Images, db.session))

with app.app_context():
    from src.models.user import User
    from src.models.model import Exam, Questions, Answers, Images
    db.init_app(app)
    db.create_all()

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)