from flaskApp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    apps = db.relationship("App", backref="owner", lazy=True)


class App(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    api_key = db.Column(db.String(32), primary_key=True, unique=True, nullable=False)
    authorization_code = db.Column(db.String(32), nullable=False)
    access_token = db.Column(db.String(32), nullable=False)
    refresh_token = db.Column(db.String(32), nullable=False)
