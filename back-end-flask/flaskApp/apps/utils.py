from flask import request, jsonify
from flask_login import current_user
from flaskApp import db
from flaskApp.config import ecobeeAppLogger
from flaskApp.models import App

import sys

sys.path.append("..")
from ecobeeApp import ecobeeApp

import json


# Apps


def get_auth(api_key):
    return ecobeeApp.requestPinAndAuthorizationCode(api_key)


def create_app():
    data = request.get_json()
    app_name = data["name"]
    api_key = data["key"]
    authorization_code = data["authorizationCode"]
    access_token, refresh_token = ecobeeApp.requestTokens(api_key, authorization_code)
    app = App(
        owner=current_user,
        name=app_name,
        api_key=api_key,
        authorization_code=authorization_code,
        access_token=access_token,
        refresh_token=refresh_token,
    )
    db.session.add(app)
    db.session.commit()


def update_app():
    data = request.get_json()
    api_key = data["api_key"]
    authorization_code = data["authorization_code"]
    access_token, refresh_token = ecobeeApp.requestTokens(api_key, authorization_code)
    app = App.query.get(api_key)
    app.authorization_code = authorization_code
    app.access_token = access_token
    app.refresh_token = refresh_token
    db.session.commit()


def delete_app(key):
    app = App.query.get(key)
    db.session.delete(app)
    db.session.commit()


def get_apps():
    apps = App.query.filter_by(owner=current_user)
    return [{"name": app.name, "key": app.api_key} for app in apps]


def getAppByKey(key):
    appConfig = App.query.get(key)
    if appConfig:
        app = ecobeeApp(config=appConfig, db=db, logger=ecobeeAppLogger)
        return app


# Thermostats


def get_user_thermostats():
    thermostats = []
    try:
        configs = App.query.filter_by(owner=current_user)
        apps = [
            ecobeeApp(config=config, db=db, logger=ecobeeAppLogger)
            for config in configs
        ]
    except:
        print("Unsuccessful app request.")
    else:
        print("Successful app request.")
        for app in apps:
            data = app.requestData()
            if data:
                thermostatList = data["thermostatList"]
                for thermostat in thermostatList:
                    thermostats.append({"api_key": app.api_key, "data": thermostat})
            else:
                print(f"{app.api_key} is not working.")
    return thermostats


def get_app_thermostats(key):
    thermostats = []
    try:
        config = App.query.get(key)
        app = ecobeeApp(config=config, db=db, logger=ecobeeAppLogger)
        data = app.requestData()
    except:
        print("Unsuccessful app request.")
    else:
        if data:
            thermostatList = data["thermostatList"]
            for thermostat in thermostatList:
                thermostats.append({"api_key": app.api_key, "data": thermostat})
        else:
            print(f"{app.api_key} is not working.")
    return thermostats


def get_thermostat(identifier):
    thermostats = get_user_thermostats()
    thermostat = next(
        (
            thermostat
            for thermostat in thermostats
            if thermostat["data"]["identifier"] == identifier
        ),
        None,
    )
    return thermostat


def get_runtime_report(key, identifier):
    appConfig = App.query.get(key)
    app = ecobeeApp(config=appConfig, db=db, logger=ecobeeAppLogger)
    data = app.getRuntimeReport(identifier)
    return jsonify(data)


# Thermostat Actions


def set_hvac_mode():
    data = json.loads(request.data.decode())
    key = data["key"]
    identifier = data["identifier"]
    mode = data["mode"]
    app = getAppByKey(key)
    return app.set_hvac_mode(identifier=identifier, hvac_mode=mode)


def resume():
    data = json.loads(request.data.decode())
    key = data["key"]
    identifier = data["identifier"]
    app = getAppByKey(key)
    return app.resume(identifier=identifier)


def set_climate():
    data = json.loads(request.data.decode())
    key = data["key"]
    identifier = data["identifier"]
    climate = data["climate"]
    app = getAppByKey(key)
    return app.set_climate_hold(identifier=identifier, climate=climate)


def set_temperature_hold():
    data = json.loads(request.data.decode())
    key = data["key"]
    identifier = data["identifier"]
    temperature = data["temperature"]
    app = getAppByKey(key)
    return app.set_temperature_hold(
        identifier=identifier, temperature=float(temperature)
    )


def send_message():
    data = json.loads(request.data.decode())
    key = data["key"]
    identifier = data["identifier"]
    message = data["message"]
    app = getAppByKey(key)
    return app.send_message(identifier=identifier, message=message)


def check_api():
    return ecobeeApp.test()
