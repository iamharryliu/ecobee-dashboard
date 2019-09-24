from flask import request, session
from flask_login import login_user, current_user, logout_user
from flaskApp import db, bcrypt
from flaskApp.models import User
import json


def register():
    data = json.loads(request.data)
    username = data["username"]
    email = data["email"]
    password = data["password"]
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()


def get_login_status():
    return current_user.is_authenticated


def login():
    data = json.loads(request.data)
    email = data["email"]
    password = data["password"]
    remember = data["remember"]
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user, remember=remember)
        return True


def logout():
    logout_user()
