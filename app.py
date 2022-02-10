from flask_login import LoginManager
from flask import render_template

from manage import app, db
from src.models.childs_exam import Childs_Answer
from src.models.user_class import Child, Parent
from src.models.user_auth import User




#blueprints
from src.views.user import auth
from src.views.admin_views import ad
from src.views.child_view import child
from src.views.parent_view import parent
from src.views.oauth import google_blueprint
from src.views.oauth import facebook_blueprint


#register blueprints
app.register_blueprint(auth)
app.register_blueprint(ad)
app.register_blueprint(child, name = 'c')
app.register_blueprint(parent, name = 'p')
app.register_blueprint(google_blueprint, url_prefix='/google')
app.register_blueprint(facebook_blueprint, url_prefix='/facebook')

login_manager = LoginManager()

with app.app_context():
    from src.models.user_class import Child, Parent
    from src.models.user_auth import User
    from src.models.childs_exam import Childs_Answer

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

@app.route('/privacy_policy')
def privacy_policy():
    return render_template("privacy_policy.html")


@app.route('/terms_of_service')
def terms_of_service():
    return render_template("terms_of_service.html")

if __name__ == '__main__':
    app.run(debug=True)