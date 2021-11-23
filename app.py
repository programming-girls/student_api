from flask_login import LoginManager

from manage import app, db
from src.users.models.student_exam import Student_Answer
from src.users.models.user import User
from src.users.models.user_class import Student, Parent

#blueprints
from src.users.views.user import auth
from src.users.views.admin_views import ad
from src.users.views.student_view import student
from src.users.views.parent_view import parent

#register blueprints
app.register_blueprint(auth)
app.register_blueprint(ad)
app.register_blueprint(student)
app.register_blueprint(parent)

login_manager = LoginManager()

with app.app_context():
    from src.users.models.user import User
    from src.users.models.user_class import Student, Parent
    from src.users.models.student_exam import Student_Answer

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