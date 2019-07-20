from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin
from flask_login import login_user, current_user, logout_user, login_required
import json
from flaskApp import db, bcrypt
from flaskApp.models import User

users_blueprint = Blueprint("users_blueprint", __name__)


def registerUser():
    data = json.loads(request.data)
    username = data["username"]
    email = data["email"]
    password = data["password"]
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()


# Register


@users_blueprint.route("/registerUser", methods=["POST"])
@cross_origin(supports_credentials=True)
def _registerUser():
    try:
        registerUser()
    except:
        success = False
    else:
        success = True
    return jsonify({"success": success})


@users_blueprint.route("/getLoggedInStatus", methods=["GET"])
@cross_origin(supports_credentials=True)
def getLoggedInStatus():
    return jsonify({"success": current_user.is_authenticated})


@users_blueprint.route("/loginUser", methods=["POST"])
@cross_origin(supports_credentials=True)
def _loginUser():
    data = json.loads(request.data)
    email = data["email"]
    password = data["password"]
    remember = data["remember"]
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user, remember=remember)
        success = True
    else:
        success = False
    return jsonify({"success": success})


@users_blueprint.route("/logoutUser", methods=["POST"])
@cross_origin(supports_credentials=True)
def _logoutUser():
    try:
        logout_user()
    except:
        success = False
    else:
        success = True
    return jsonify({"success": success})
