from flaskApp.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
admin = Admin()
login_manager = LoginManager()
# login_manager.session_protection = None
# login_manager.login_view = "users_blueprint.login"
# login_manager.login_message_category = "info"
bcrypt = Bcrypt()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(Config)

    # Connect Database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Admin Views
    admin.init_app(app)
    from flaskApp.models import User, App
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(App, db.session))

    # Login Manager and Bcrypt
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Blueprint Routes
    from flaskApp.apps.routes import apps_blueprint
    from flaskApp.users.routes import users_blueprint
    app.register_blueprint(apps_blueprint, url_prefix='/apps')
    app.register_blueprint(users_blueprint, url_prefix='/users')

    return app
