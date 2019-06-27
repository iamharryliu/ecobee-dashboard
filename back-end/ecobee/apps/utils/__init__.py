from flask import abort
from ecobee import db
from ecobee.config import logger, temp_log_dir, occupancy_log_dir
from ecobee.models import apis
from ecobee.apps.utils.thermostat_utils import Thermostat

from ecobeeAPI import EcobeeAPI


def addApp(request):
    name = request.form["name"]
    api_key = request.form["api_key"]
    authorization_code = request.form["authorization_code"]
    access_token = request.form["access_token"]
    refresh_token = request.form["refresh_token"]
    app = EcobeeAPI(name=name, api_key=api_key, authorization_code=authorization_code, access_token=access_token, refresh_token=refresh_token, logger=logger)
    if app.data:
        app = apis(
            name=name,
            api_key=api_key,
            authorization_code=authorization_code,
            access_token=access_token,
            refresh_token=refresh_token
        )
        db.session.add(app)
        db.session.commit()
        return True
    else:
        return False


def getAPIs():
    return apis.query.all()


def getAppConfig(app_name):
    return apis.query.filter_by(name=app_name).first()


def getApp(app_name):
    app_config = getAppConfig(app_name)
    if app_config:
        app = EcobeeAPI(config=app_config, db=db, logger=logger)
        return app
    else:
        abort(404)


def deleteAPI(name):
    app = getAppConfig(name)
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
