from flask import abort, request
from flask_login import current_user
from flaskApp import db
from flaskApp.config import ecobeeAppLogger, temp_log_dir, occupancy_log_dir
from flaskApp.models import App
from flaskApp.apps.utils.thermostat_utils import Thermostat

from ecobeeApp import ecobeeApp

def createApp():
    data = request.get_json()
    app_name = data['appName']
    api_key = data['apiKey']
    authorization_code = data['authorizationCode']
    print(app_name,api_key,authorization_code)
    access_token, refresh_token = ecobeeApp.requestTokens(api_key, authorization_code)
    app = App(
        owner=current_user,
        name=app_name,
        api_key=api_key,
        authorization_code=authorization_code,
        access_token=access_token,
        refresh_token=refresh_token
    )
    db.session.add(app)
    db.session.commit()


def getApps():
    ''' get Apps (names and keys) '''
    apps = App.query.all()
    apps = [{'name':app.name, 'key':app.api_key} for app in apps]
    return apps

def getAppConfigByKey(key):
    ''' get App config by key. '''
    return App.query.filter_by(api_key=key).first()


def getAppByKey(key):
    ''' Get App by key. '''
    appConfig = getAppConfigByKey(key)
    if appConfig:
        app = ecobeeApp(config=appConfig, db=db, logger=ecobeeAppLogger)
        return app
    else:
        abort(404)


def deleteApp(api_key):
    ''' Delete App by key. '''
    app = getAppConfigByKey(api_key)
    db.session.delete(app)
    db.session.commit()


def getThermostats(api):
    thermostats = []
    thermostats_data = api.data['thermostatList']
    for thermostat_data in thermostats_data:
        thermostat_data['temp_log_dir'] = temp_log_dir
        thermostat_data['occupancy_log_dir'] = occupancy_log_dir
        thermostat = Thermostat(thermostat_data)
        thermostats.append(thermostat)
    return thermostats


def getThermostat(thermostats, identifier):
    thermostat = next((thermostat for thermostat in thermostats if thermostat.identifier == identifier), None)
    if thermostat:
        return thermostat
    else:
        abort(404)
