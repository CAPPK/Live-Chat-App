
from flask_login import LoginManager
from flask import Flask
from google.cloud import datastore
datastore_client = datastore.Client()


def create_app():
    """Construct the core app object."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super secret key'

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, getUser

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return getUser(user_id)

    return app
