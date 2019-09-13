from flask import request
from flask_login import current_user
from flaskApp import db
from flaskApp.config import ecobeeAppLogger
from flaskApp.models import App

from ecobeeApp import ecobeeApp

def createApp():
    data = request.get_json()
    app_name = data['name']
    api_key = data['key']
    authorization_code = data['authorizationCode']
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

def getUserApps():
    apps = App.query.filter_by(owner=current_user)
    return apps

def getApp(key):
    app = App.query.filter_by(owner=current_user, api_key=key)
    return app
    
def getAppConfigByKey(key):
    ''' get App config by key. '''
    return App.query.filter_by(api_key=key).first()


def getAppByKey(key):
    ''' Get App by key. '''
    appConfig = getAppConfigByKey(key)
    if appConfig:
        app = ecobeeApp(config=appConfig, db=db, logger=ecobeeAppLogger)
        return app

def deleteApp(api_key):
    ''' Delete App by key. '''
    app = getAppConfigByKey(api_key)
    db.session.delete(app)
    db.session.commit()
 
def getUserThermostats():
    thermostats = []
    appConfigs = getUserApps()
    for appConfig in appConfigs:
        app = ecobeeApp(config=appConfig, db=db, logger=ecobeeAppLogger)
        data = app.requestData()
        if data:
            thermostatList = data['thermostatList']
            for thermostat in thermostatList:
                thermostats.append({'api_key':appConfig.api_key,'data':thermostat})
        else:
            print(f'{appConfig.api_key} is not working.')
    return thermostats

def getAppThermostats(key):
    thermostats = []
    appConfig = getApp(key)[0]
    app = ecobeeApp(config=appConfig, db=db, logger=ecobeeAppLogger)
    data = app.requestData()
    if data:
        thermostatList = data['thermostatList']
        for thermostat in thermostatList:
            thermostats.append({'api_key':appConfig.api_key,'data':thermostat})
    else:
        print(f'{appConfig.api_key} is not working.')
    return thermostats

def getThermostat(thermostats, identifier):
    thermostat = next((thermostat for thermostat in thermostats if thermostat.identifier == identifier), None)
    if thermostat:
        return thermostat
    else:
        return None