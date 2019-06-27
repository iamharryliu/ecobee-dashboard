from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from ecobee.config import Config

db = SQLAlchemy()
cors = CORS()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(Config)

    db.init_app(app)
    cors.init_app(app)

    with app.app_context():
        db.create_all()

    from ecobee.main.routes import main
    from ecobee.apps.routes import apps_blueprint

    app.register_blueprint(main)
    app.register_blueprint(apps_blueprint)

    return app
