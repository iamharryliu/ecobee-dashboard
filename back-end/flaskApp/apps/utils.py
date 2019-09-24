from flask import request, jsonify
from flask_login import current_user
from flaskApp import db
from flaskApp.config import ecobeeAppLogger
from flaskApp.models import App
from ecobeeApp import ecobeeApp


def get_app_auth(api_key):
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


def update_app_credentials():
    data = request.get_json()
    api_key = data["api_key"]
    authorization_code = data["authorization_code"]
    access_token, refresh_token = ecobeeApp.requestTokens(api_key, authorization_code)
    app = App.query.get(api_key)
    app.authorization_code = authorization_code
    app.access_token = access_token
    app.refresh_token = refresh_token
    db.session.commit()


def getApps():
    apps = App.query.all()
    apps = [{"name": app.name, "key": app.api_key} for app in apps]
    return apps


def get_user_configs():
    apps = App.query.filter_by(owner=current_user)
    return [{"name": app.name, "key": app.api_key} for app in apps]


def getAppConfig(key):
    return App.query.get(key)


def getAppByKey(key):
    appConfig = getAppConfig(key)
    if appConfig:
        app = ecobeeApp(config=appConfig, db=db, logger=ecobeeAppLogger)
        return app


def delete_app(key):
    app = getAppConfig(key)
    db.session.delete(app)
    db.session.commit()


def get_user_thermostats():
    thermostats = []
    configs = App.query.filter_by(owner=current_user)
    apps = [
        ecobeeApp(config=config, db=db, logger=ecobeeAppLogger) for config in configs
    ]
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
    config = getAppConfig(key)
    app = ecobeeApp(config=config, db=db, logger=ecobeeAppLogger)
    data = app.requestData()
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


def getRuntimeReport(key, identifier):
    appConfig = App.query.get(key)
    app = ecobeeApp(config=appConfig, db=db, logger=ecobeeAppLogger)
    data = app.getRuntimeReport(identifier)
    return jsonify(data)
