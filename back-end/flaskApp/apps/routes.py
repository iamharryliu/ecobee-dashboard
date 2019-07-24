from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flaskApp.apps.utils import (
    createApp,
    deleteApp,
    getUserApps,
    getAppByKey,
    getThermostats,
    getUserThermostats,
    getThermostat,
)
from flask_login import login_required

from ecobeeApp import ecobeeApp

apps_blueprint = Blueprint("apps_blueprint", __name__, template_folder="templates")


# Register


@apps_blueprint.route("/apps/authorize/<string:api_key>", methods=["GET"])
@cross_origin(supports_credentials=True)
@login_required
def _authorizeApp(api_key):
    try:
        pin, authorization_code = ecobeeApp.requestPinAndAuthorizationCode(api_key)
    except:
        success = False
        data = None
    else:
        success = True
        data = {"pin": pin, "authorization_code": authorization_code}
    r = {"success": success, "data": data}
    return jsonify(r)


@apps_blueprint.route("/apps/create", methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required
def _createApp():
    try:
        createApp()
    except Exception as e:
        print(e)
        success = False
    else:
        success = True
    return jsonify({"success": success})


@apps_blueprint.route("/apps/delete/<string:api_key>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def _deleteApp(api_key):
    try:
        deleteApp(api_key)
    except:
        success = False
    else:
        success = True
    return jsonify({"success": success})


@apps_blueprint.route("/apps", methods=["GET"])
@cross_origin(supports_credentials=True)
@login_required
def _getUserApps():
    apps = getUserApps()
    apps = [{"name": app.name, "key": app.api_key} for app in apps]
    return jsonify(apps)


@apps_blueprint.route("/getUserThermostats")
@cross_origin(supports_credentials=True)
@login_required
def _getUserThermostats():
    thermostats = getUserThermostats()
    return jsonify(thermostats)


@apps_blueprint.route("/fetchThermostat/<key>/<identifier>")
@cross_origin(supports_credentials=True)
def _fetchThermostatByIdentifier(key, identifier):
    app = getAppByKey(key)
    thermostats = getThermostats(app)
    thermostat = getThermostat(thermostats, identifier)
    set = {
        "key": key,
        "identifier": identifier,
        "name": thermostat.name,
        "temperature": thermostat.actual_temperature,
        "hvacMode": thermostat.hvac_mode,
        "currentClimateData": thermostat.current_climate_data.data,
        "remoteSensors": thermostat.getRemoteSensorData(),
        "sensor": thermostat.getSensorData(),
        "climates": ["away", "home", "sleep"],
    }
    return jsonify(set)


# Front-end actions

import json


@apps_blueprint.route("/setHvacMode", methods=["POST"])
@cross_origin(supports_credentials=True)
def setHvacMode():
    data = json.loads(request.data.decode())
    key = data["key"]
    identifier = data["identifier"]
    mode = data["mode"]
    app = getAppByKey(key)
    r = app.set_hvac_mode(identifier=identifier, hvac_mode=mode)
    message = f"HVAC mode set to {mode}."
    return jsonify({"success": r, "message": message})


@apps_blueprint.route("/resume", methods=["POST"])
@cross_origin(supports_credentials=True)
def resume():
    data = json.loads(request.data.decode())
    key = data["key"]
    identifier = data["identifier"]
    app = getAppByKey(key)
    r = app.resume(identifier=identifier)
    message = f"Regular program resumed."
    return jsonify({"success": r, "message": message})


@apps_blueprint.route("/setClimate", methods=["POST"])
@cross_origin(supports_credentials=True)
def setClimate():
    data = json.loads(request.data.decode())
    key = data["key"]
    identifier = data["identifier"]
    climate = data["climate"]
    app = getAppByKey(key)
    r = app.set_climate_hold(identifier=identifier, climate=climate)
    message = f"Climate set to {climate}."
    return jsonify({"success": r, "message": message})


@apps_blueprint.route("/setTemperature", methods=["POST"])
@cross_origin(supports_credentials=True)
def setTemperatureHold():
    data = json.loads(request.data.decode())
    key = data["key"]
    identifier = data["identifier"]
    temperature = data["temperature"]
    app = getAppByKey(key)
    r = app.set_temperature_hold(identifier=identifier, temperature=float(temperature))
    message = f"Temperature set to {temperature}C."
    return jsonify({"success": r, "message": message})


@apps_blueprint.route("/sendMessage", methods=["POST"])
@cross_origin(supports_credentials=True)
def sendMessage():
    data = json.loads(request.data.decode())
    key = data["key"]
    identifier = data["identifier"]
    message = data["message"]
    app = getAppByKey(key)
    r = app.send_message(identifier=identifier, message=message)
    message = f"Message sent."
    return jsonify({"success": r, "message": message})

