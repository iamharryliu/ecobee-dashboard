from flask import Blueprint, jsonify, request
from flask_login import login_required
from flask_cors import cross_origin
from flaskApp.apps.utils import (
    get_auth,
    create_app,
    update_app,
    delete_app,
    get_apps,
    getAppByKey,
    get_user_thermostats,
    get_app_thermostats,
    get_thermostat,
    get_runtime_report,
    set_hvac_mode,
    resume,
    set_climate,
    set_temperature_hold,
    send_message,
    check_api,
)

apps_blueprint = Blueprint("apps_blueprint", __name__)


# Apps

import requests


@apps_blueprint.route("/checkAPI", methods=["GET"])
@cross_origin(supports_credentials=True)
def _check_api():
    if check_api():
        success = True
    else:
        success = False
    return jsonify({"success": success})


@apps_blueprint.route("/authorize/<string:api_key>", methods=["GET"])
@cross_origin(supports_credentials=True)
def _get_auth(api_key):
    try:
        pin, authorization_code = get_auth(api_key)
    except:
        print("Unsuccessfuly authorized app.")
        success = False
        data = None
    else:
        print("Successfully authorized app.")
        success = True
        data = {"pin": pin, "authorization_code": authorization_code}
    return jsonify({"success": success, "data": data})


@apps_blueprint.route("/create", methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required
def _create_app():
    try:
        create_app()
    except:
        print("Unsuccessfully created app.")
        success = False
    else:
        print("Successfully created app.")
        success = True
    return jsonify({"success": success})


@apps_blueprint.route("/updateCredentials", methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required
def _update():
    try:
        update_app()
    except:
        print("Unsuccessfully updated app.")
        success = False
    else:
        print("Successfully updated app.")
        success = True
    return jsonify({"success": success})


@apps_blueprint.route("/delete/<string:api_key>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def _delete_app(api_key):
    try:
        delete_app(api_key)
    except:
        print("Unsuccessfully deleted app.")
        success = False
    else:
        print("Successfully deleted app.")
        success = True
    return jsonify({"success": success})


@apps_blueprint.route("", methods=["GET"])
@cross_origin(supports_credentials=True)
@login_required
def _get_apps():
    apps = get_apps()
    return jsonify(apps)


# Thermostats


@apps_blueprint.route("/getUserThermostats")
@cross_origin(supports_credentials=True)
@login_required
def _getUserThermostats():
    thermostats = get_user_thermostats()
    return jsonify(thermostats)


@apps_blueprint.route("/getAppThermostats/<string:key>")
@cross_origin(supports_credentials=True)
@login_required
def _get_app_thermostats(key):
    thermostats = get_app_thermostats(key)
    return jsonify(thermostats)


@apps_blueprint.route("/thermostat/<identifier>")
@cross_origin(supports_credentials=True)
@login_required
def _get_thermostat(identifier):
    thermostat = get_thermostat(identifier)
    success = True if thermostat else False
    return jsonify({"success": success, "thermostat": thermostat})


@apps_blueprint.route(
    "/thermostats/<string:key>/<string:identifier>/runtimeReport", methods=["GET"]
)
@cross_origin(supports_credentials=True)
@login_required
def _get_runtime_report(key, identifier):
    return get_runtime_report(key, identifier)


# Thermostat Actions


@apps_blueprint.route("/setHvacMode", methods=["POST"])
@cross_origin(supports_credentials=True)
def _set_hvac_mode():
    return jsonify({"success": set_hvac_mode()})


@apps_blueprint.route("/resume", methods=["POST"])
@cross_origin(supports_credentials=True)
def _resume():
    return jsonify({"success": resume()})


@apps_blueprint.route("/setClimate", methods=["POST"])
@cross_origin(supports_credentials=True)
def _set_climate():
    return jsonify({"success": set_climate()})


@apps_blueprint.route("/setTemperature", methods=["POST"])
@cross_origin(supports_credentials=True)
def _set_temperature_hold():
    return jsonify({"success": set_temperature_hold()})


@apps_blueprint.route("/sendMessage", methods=["POST"])
@cross_origin(supports_credentials=True)
def _send_message():
    return jsonify({"success": send_message()})
