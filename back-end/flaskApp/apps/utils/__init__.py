from flask import request, jsonify
from flask_login import current_user
from flaskApp import db
from flaskApp.config import ecobeeAppLogger
from flaskApp.models import App
from ecobeeApp import ecobeeApp


def createApp():
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

def updateAppCredentials(api_key, authorization_code, access_token, refresh_token):
    app = App.query.get(api_key)
    app.authorization_code = authorization_code
    app.access_token = access_token
    app.refresh_token = refresh_token
    db.session.commit()

def getApps():
    """ get Apps (names and keys) """
    apps = App.query.all()
    apps = [{"name": app.name, "key": app.api_key} for app in apps]
    return apps


def getUserConfigs():
    apps = App.query.filter_by(owner=current_user)
    return [{"name": app.name, "key": app.api_key} for app in apps]


def getAppConfig(key):
    """ get App config by key. """
    return App.query.get(key)


def getAppByKey(key):
    """ Get App by key. """
    appConfig = getAppConfig(key)
    if appConfig:
        app = ecobeeApp(config=appConfig, db=db, logger=ecobeeAppLogger)
        return app


def deleteApp(key):
    """ Delete App by key. """
    app = getAppConfig(key)
    db.session.delete(app)
    db.session.commit()


def getUserThermostats():
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


def getAppThermostats(key):
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

def getRuntimeReport(key, identifier):
    appConfig = App.query.get(key)
    app = ecobeeApp(config=appConfig, db=db, logger=ecobeeAppLogger)
    data = app.getRuntimeReport(identifier)
    return jsonify(data)
