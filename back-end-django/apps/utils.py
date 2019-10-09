from .models import App

import sys

sys.path.append("../")
from ecobeeApp import ecobeeApp

import json


# Apps


def check_api():
    return ecobeeApp.test()


def authorize(api_key):
    return ecobeeApp.requestPinAndAuthorizationCode(api_key)


def create_app(request):
    data = json.loads(request.body)
    app_name = data["name"]
    api_key = data["key"]
    authorization_code = data["authorizationCode"]
    access_token, refresh_token = ecobeeApp.requestTokens(api_key, authorization_code)
    app = App(
        owner=request.user,
        name=app_name,
        api_key=api_key,
        authorization_code=authorization_code,
        access_token=access_token,
        refresh_token=refresh_token,
    )
    app.save()


def update_app(request):
    data = json.loads(request.body)
    key = data["api_key"]
    authorization_code = data["authorization_code"]
    access_token, refresh_token = ecobeeApp.requestTokens(key, authorization_code)
    app = App.objects.get(api_key=key)
    app.authorization_code = authorization_code
    app.access_token = access_token
    app.refresh_token = refresh_token
    app.save()


def delete_app(key):
    app = App.objects.get(api_key=key)
    app.delete()


def get_apps(request):
    apps = App.objects.filter(owner=request.user)
    return [{"name": app.name, "key": app.api_key} for app in apps]


def getAppByKey(key):
    appConfig = App.objects.get(api_key=key)
    if appConfig:
        app = ecobeeApp(config=appConfig, dbType="Django")
        return app


# # Thermostats


def get_user_thermostats(request):
    thermostats = []
    try:
        configs = App.objects.filter(owner=request.user)
        apps = [ecobeeApp(config=config, dbType="Django") for config in configs]
        print(apps)
    except:
        print("Unsuccessful request.")
    else:
        print("Successful request.")
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
        config = App.objects.get(api_key=key)
        app = ecobeeApp(config=config, dbType="Django")
        data = app.requestData()
    except:
        print("Unsuccessful request.")
    else:
        print("Successful request.")
        if data:
            thermostatList = data["thermostatList"]
            for thermostat in thermostatList:
                thermostats.append({"api_key": app.api_key, "data": thermostat})
        else:
            print(f"{app.api_key} is not working.")
    return thermostats


def get_thermostat(request, identifier):
    thermostats = get_user_thermostats(request)
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
    appConfig = App.objects.get(api_key=key)
    app = ecobeeApp(config=appConfig, dbType="Django")
    data = app.getRuntimeReport(identifier)
    return data


# Thermostat Actions


def set_hvac_mode(request):
    data = json.loads(request.body)
    key = data["key"]
    identifier = data["identifier"]
    mode = data["mode"]
    app = getAppByKey(key)
    return app.set_hvac_mode(identifier=identifier, hvac_mode=mode)


def resume(request):
    data = json.loads(request.body)
    key = data["key"]
    identifier = data["identifier"]
    app = getAppByKey(key)
    return app.resume(identifier=identifier)

def set_climate(request):
    data = json.loads(request.body)
    key = data["key"]
    identifier = data["identifier"]
    climate = data["climate"]
    app = getAppByKey(key)
    return app.set_climate_hold(identifier=identifier, climate=climate)


def set_temperature_hold(request):
    data = json.loads(request.body)
    key = data["key"]
    identifier = data["identifier"]
    temperature = data["temperature"]
    app = getAppByKey(key)
    return app.set_temperature_hold(
        identifier=identifier, temperature=float(temperature)
    )


def send_message(request):
    data = json.loads(request.body)
    key = data["key"]
    identifier = data["identifier"]
    message = data["message"]
    app = getAppByKey(key)
    return app.send_message(identifier=identifier, message=message)