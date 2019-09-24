from flask import Blueprint, jsonify
from flask_cors import cross_origin
from flaskApp.users.utils import register, get_login_status, login, logout

users_blueprint = Blueprint("users_blueprint", __name__)


@users_blueprint.route("/registerUser", methods=["POST"])
@cross_origin(supports_credentials=True)
def _register():
    try:
        register()
    except:
        success = False
    else:
        success = True
    return jsonify({"success": success})


@users_blueprint.route("/getLoggedInStatus", methods=["GET"])
@cross_origin(supports_credentials=True)
def _get_login_status():
    status = get_login_status()
    return jsonify({"success": status})


@users_blueprint.route("/loginUser", methods=["POST"])
@cross_origin(supports_credentials=True)
def _login():
    try:
        success = login()
    except:
        success = False
    else:
        pass
    return jsonify({"success": success})


@users_blueprint.route("/logoutUser", methods=["POST"])
@cross_origin(supports_credentials=True)
def _logout():
    try:
        logout()
    except:
        success = False
    else:
        success = True
    return jsonify({"success": success})
