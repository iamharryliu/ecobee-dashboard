from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_cors import cross_origin
from ecobee.config import TEMPERATURE_OPTIONS
from ecobee.apps.forms import EcobeeAppForm
from ecobee.apps.utils import addApp, getApp, getAppConfig, getAPIs, deleteAPI, getThermostats, getThermostat

from ecobeeAPI import EcobeeAPI

apps_blueprint = Blueprint("apps_blueprint", __name__, template_folder='templates')

# Apps


@apps_blueprint.route("/apps")
def apps():
    apps = getAPIs()
    return render_template("apps/view.html", apps=apps)


@apps_blueprint.route("/apps/add", methods=["GET", "POST"])
def add_app():
    form = EcobeeAppForm()
    if form.validate_on_submit():
        if addApp(request):
            flash('Successfully registered API', 'success')
            return redirect(url_for("main.home"))
        else:
            flash('Failed to register API', 'danger')
            return redirect(url_for('apps_blueprint.add_app'))
    return render_template("apps/components/add-app.html", form=form)


@apps_blueprint.route("/apps/<name>/edit", methods=["GET", "POST"])
def edit_app(name):
    app = getAppConfig(name)
    form = EcobeeAppForm()
    form.name.data = app.name
    form.api_key.data = app.api_key
    form.authorization_code.data = app.authorization_code
    form.access_token.data = app.access_token
    form.refresh_token.data = app.refresh_token
    return render_template("apps/components/edit-app.html", form=form)


@apps_blueprint.route("/apps/<name>/delete", methods=["POST"])
def delete_app(name):
    deleteAPI(name)
    return redirect(url_for("apps_blueprint.apps"))


# Thermostats


@apps_blueprint.route("/apps/<key>/")
@apps_blueprint.route("/apps/<key>/thermostats/")
def thermostats(key):
    app = getApp(key)
    thermostats = getThermostats(app)
    return render_template("thermostats/view.html", app=app, thermostats=thermostats)


@apps_blueprint.route(
    "/apps/<key>/thermostats/<identifier>/",
    methods=["GET", "POST"],
)
def thermostat(key, identifier):
    app = getApp(key)
    thermostats = getThermostats(app)
    thermostat = getThermostat(thermostats, identifier)
    temperatures_chart = thermostat.get_thermostat_temperature_chart_data(app.api_key)
    occupancy_chart = thermostat.get_occupancy_chart_data(app.api_key)

    return render_template(
        "thermostats/thermostat/view.html",
        key=app.api_key,
        app=app,
        thermostat=thermostat,
        temperature_options=TEMPERATURE_OPTIONS,
        temperature_chart=temperatures_chart,
        occupancy_chart=occupancy_chart
    )


# Thermostat Actions


@apps_blueprint.route(
    "/apps/<key>/thermostats/<identifier>/resume",
    methods=["POST"],
)
def resume(key, identifier):
    app = getApp(key)
    app.resume(identifier=identifier)
    return redirect(
        url_for(
            "apps_blueprint.thermostat",
            key=key,
            identifier=identifier,
        )
    )


@apps_blueprint.route(
    "/apps/<key>/thermostats/<identifier>/set_hvac_mode",
    methods=["POST"],
)
def set_hvac_mode(key, identifier):
    app = getApp(key)
    hvac_mode = request.form["hvac_mode"]
    app.set_hvac_mode(identifier=identifier, hvac_mode=hvac_mode)
    return redirect(
        url_for(
            "apps_blueprint.thermostat",
            key=key,
            identifier=identifier,
        )
    )


@apps_blueprint.route(
    "/apps/<key>/thermostats/<identifier>/send_message",
    methods=["POST"],
)
def send_message(key, identifier):
    app = getApp(key)
    message = request.form["message"]
    app.send_message(identifier=identifier, message=message)
    flash('Message sent to thermostat.', 'success')
    return redirect(
        url_for(
            "apps_blueprint.thermostat",
            key=key,
            identifier=identifier,
        )
    )


@apps_blueprint.route(
    "/apps/<key>/thermostats/<identifier>/set_climate_hold",
    methods=["POST"],
)
def set_climate_hold(key, identifier):
    app = getApp(key)
    climate = request.form["climate"]
    app.set_climate_hold(identifier=identifier, climate=climate)
    return redirect(
        url_for(
            "apps_blueprint.thermostat",
            key=key,
            identifier=identifier,
        )
    )


@apps_blueprint.route(
    "/apps/<key>/thermostats/<identifier>/set_temperature_hold",
    methods=["POST"],
)
def set_temperature_hold(key, identifier):
    app = getApp(key)
    temperature = request.form["temperature"]
    temperature = float(temperature)
    app.set_temperature_hold(identifier=identifier, temperature=temperature)
    return redirect(
        url_for(
            "apps_blueprint.thermostat",
            key=key,
            identifier=identifier,
        )
    )

# Fetch for front-end


@apps_blueprint.route("/fetchAPIs")
@cross_origin()
def fetchAPIs():
    apis = getAPIs()
    set = []
    for api in apis:
        set.append({'name': api.name, 'key': api.api_key})
    return jsonify(set)


@apps_blueprint.route("/fetchThermostats/<key>")
@cross_origin()
def fetchThermostats(key):
    app = getApp(key)
    thermostats = getThermostats(app)
    set = []
    for thermostat in thermostats:
        set.append({
            'name': thermostat.name,
            'key': key,
            'identifier': thermostat.identifier}
        )
    return jsonify(set)


@apps_blueprint.route("/fetchThermostat/<key>/<identifier>")
@cross_origin()
def fetchThermostat(key, identifier):
    app = getApp(key)
    thermostats = getThermostats(app)
    thermostat = getThermostat(thermostats, identifier)
    set = {
        'key': key,
        'identifier': identifier,
        'name': thermostat.name,
        'temperature': thermostat.actual_temperature,
        'hvacMode': thermostat.hvac_mode,
        'currentClimateData': thermostat.current_climate_data.data,
        'remoteSensors': thermostat.getRemoteSensorData(),
        'sensor': thermostat.getSensorData(),
        'climates': ['away', 'home', 'sleep']
    }
    return jsonify(set)

# Front-end actions


@apps_blueprint.route("/addApp", methods=["POST"])
@cross_origin()
def addApp():
    form = EcobeeAppForm()
    if form.validate_on_submit():
        if addApp(request):
            return jsonify({'success': True})
        else:
            print(1)
            return jsonify({'success': False})
    print(2)
    return jsonify({'success': False})


@apps_blueprint.route(
    "/setHvacMode/<key>/<identifier>/<mode>",
    methods=["POST"],
)
@cross_origin()
def setHvacMode(key, identifier, mode):
    app = getApp(key)
    r = app.set_hvac_mode(identifier=identifier, hvac_mode=mode)
    message = f'HVAC mode set to {mode}.'
    return jsonify({'success': r, 'message': message})


@apps_blueprint.route(
    "/resume/<key>/<identifier>",
    methods=["POST"])
@cross_origin()
def resume2(key, identifier):
    app = getApp(key)
    r = app.resume(identifier=identifier)
    message = f'Regular program resumed.'
    return jsonify({'success': r, 'message': message})


@apps_blueprint.route(
    "/setClimate/<key>/<identifier>/<climate>",
    methods=["POST"],
)
@cross_origin()
def setClimate(key, identifier, climate):
    app = getApp(key)
    r = app.set_climate_hold(identifier=identifier, climate=climate)
    message = f'Climate set to {climate}.'
    return jsonify({'success': r, 'message': message})


@apps_blueprint.route(
    "/setTemperature/<key>/<identifier>/<temperature>",
    methods=["POST"],
)
@cross_origin()
def setTemperatureHold(key, identifier, temperature):
    app = getApp(key)
    r = app.set_temperature_hold(identifier=identifier, temperature=float(temperature))
    message = f'Temperature set to {temperature}C.'
    return jsonify({'success': r, 'message': message})


@apps_blueprint.route(
    "/sendMessage/<key>/<identifier>/<message>",
    methods=["POST"],
)
@cross_origin()
def sendMessage(key, identifier, message):
    app = getApp(key)
    r = app.send_message(identifier=identifier, message=message)
    message = f'Message sent.'
    return jsonify({'success': r, 'message': message})
