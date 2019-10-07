from flask import Blueprint, jsonify
from flask_cors import cross_origin
from flaskApp.users.utils import register, get_login_status, login, logout

users_blueprint = Blueprint("users_blueprint", __name__)


@users_blueprint.route("/register", methods=["POST"])
@cross_origin(supports_credentials=True)
def _register():
    try:
        register()
    except:
        success = False
    else:
        success = True
    return jsonify({"success": success})


@users_blueprint.route("/loginStatus", methods=["GET"])
@cross_origin(supports_credentials=True)
def _login_status():
    status = get_login_status()
    return jsonify({"success": True, "status": status})


@users_blueprint.route("/login", methods=["POST"])
@cross_origin(supports_credentials=True)
def _login():
    success = True if login() else False
    return jsonify({"success": success})


@users_blueprint.route("/logout", methods=["POST"])
@cross_origin(supports_credentials=True)
def _logout():
    logout()
    return jsonify({"success": True})
