from flask import Blueprint, render_template, redirect, url_for, flash, request
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


@apps_blueprint.route("/apps/<string:name>/edit", methods=["GET", "POST"])
def edit_app(name):
    app = getAppConfig(name)
    form = EcobeeAppForm()
    form.name.data = app.name
    form.api_key.data = app.api_key
    form.authorization_code.data = app.authorization_code
    form.access_token.data = app.access_token
    form.refresh_token.data = app.refresh_token
    return render_template("apps/components/edit-app.html", form=form)


@apps_blueprint.route("/apps/<string:name>/delete", methods=["POST"])
def delete_app(name):
    deleteAPI(name)
    return redirect(url_for("apps_blueprint.apps"))


# Thermostats


@apps_blueprint.route("/apps/<string:app_name>/")
@apps_blueprint.route("/apps/<string:app_name>/thermostats/")
def thermostats(app_name):
    app = getApp(app_name)
    thermostats = getThermostats(app)
    return render_template("thermostats/view.html", app=app, thermostats=thermostats)


@apps_blueprint.route(
    "/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/",
    methods=["GET", "POST"],
)
def thermostat(app_name, thermostat_identifier):

    app = getApp(app_name)
    thermostats = getThermostats(app)
    thermostat = getThermostat(thermostats, thermostat_identifier)
    temperatures_chart = thermostat.get_thermostat_temperature_chart_data(app.api_key)
    occupancy_chart = thermostat.get_occupancy_chart_data(app.api_key)

    return render_template(
        "thermostats/thermostat/view.html",
        app_name=app_name,
        app=app,
        thermostat=thermostat,
        temperature_options=TEMPERATURE_OPTIONS,
        temperature_chart=temperatures_chart,
        occupancy_chart=occupancy_chart
    )


# Thermostat Actions


@apps_blueprint.route(
    "/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/resume",
    methods=["POST"],
)
def resume(app_name, thermostat_identifier):
    app = getApp(app_name)
    app.resume(identifier=thermostat_identifier)
    return redirect(
        url_for(
            "apps_blueprint.thermostat",
            app_name=app_name,
            thermostat_identifier=thermostat_identifier,
        )
    )


@apps_blueprint.route(
    "/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/set_hvac_mode",
    methods=["POST"],
)
def set_hvac_mode(app_name, thermostat_identifier):
    app = getApp(app_name)
    hvac_mode = request.form["hvac_mode"]
    app.set_hvac_mode(identifier=thermostat_identifier, hvac_mode=hvac_mode)
    return redirect(
        url_for(
            "apps_blueprint.thermostat",
            app_name=app_name,
            thermostat_identifier=thermostat_identifier,
        )
    )


@apps_blueprint.route(
    "/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/send_message",
    methods=["POST"],
)
def send_message(app_name, thermostat_identifier):
    app = getApp(app_name)
    message = request.form["message"]
    app.send_message(identifier=thermostat_identifier, message=message)
    flash('Message sent to thermostat.', 'success')
    return redirect(
        url_for(
            "apps_blueprint.thermostat",
            app_name=app_name,
            thermostat_identifier=thermostat_identifier,
        )
    )


@apps_blueprint.route(
    "/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/set_climate_hold",
    methods=["POST"],
)
def set_climate_hold(app_name, thermostat_identifier):
    app = getApp(app_name)
    climate = request.form["climate"]
    app.set_climate_hold(identifier=thermostat_identifier, climate=climate)
    return redirect(
        url_for(
            "apps_blueprint.thermostat",
            app_name=app_name,
            thermostat_identifier=thermostat_identifier,
        )
    )


@apps_blueprint.route(
    "/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/set_temperature_hold",
    methods=["POST"],
)
def set_temperature_hold(app_name, thermostat_identifier):
    app = getApp(app_name)
    temperature = request.form["temperature"]
    temperature = float(temperature)
    app.set_temperature_hold(identifier=thermostat_identifier, temperature=temperature)
    return redirect(
        url_for(
            "apps_blueprint.thermostat",
            app_name=app_name,
            thermostat_identifier=thermostat_identifier,
        )
    )
