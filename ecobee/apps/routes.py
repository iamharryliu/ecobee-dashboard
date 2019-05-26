from flask import Blueprint, render_template, redirect, url_for, flash, request
from ecobee import db
from ecobee.models import apis
from ecobee.apps.utils import Ecobee_API, temperature_options
from ecobee.apps.forms import EcobeeAppForm
import csv

apps_blueprint = Blueprint("apps_blueprint", __name__, template_folder='templates')


def get_graph_data(app):
    temperatures_slice = slice(-24, None)
    thermostat = app.get_thermostats()[0]
    series = []
    categories = []
    with open(f'ecobee/logs/{app.api_key}-{thermostat.identifier}-{thermostat.sensor.id[0:2] + thermostat.sensor.id[-1:]}') as f:
        temperatures = []
        reader = csv.reader(f)
        for line in reader:
            categories.append(line[0][-6:])
            temperatures.append(float(line[1]))
    thermostat_data = {"name": thermostat.name, "data": temperatures[temperatures_slice]}
    series.append(thermostat_data)
    with open(f'ecobee/logs/{app.api_key}-{thermostat.identifier}-{thermostat.sensor.id[0:2] + thermostat.sensor.id[-1:]}') as f:
        temperatures = []
        reader = csv.reader(f)
        for line in reader:
            temperatures.append(float(line[2]))
    thermostat_data = {"name": 'Set Temperature', "data": temperatures[temperatures_slice]}
    series.append(thermostat_data)
    for sensor in thermostat.remote_sensors:
        try:
            with open(f'ecobee/logs/{app.api_key}-{thermostat.identifier}-{sensor.id[0:2] + sensor.id[-3:]}', 'r') as f:
                reader = csv.reader(f)
                temperatures = list(float(line[1]) if line[1] != '' else '' for line in reader)
            sensor_data = {"name": sensor.name, "data": temperatures[temperatures_slice]}
            series.append(sensor_data)
        except Exception as e:
            print(e)
    return categories[temperatures_slice], series

# Apps


@apps_blueprint.route("/apps")
def apps():
    apps = apis.query.all()
    return render_template("apps/view.html", apps=apps)


@apps_blueprint.route("/apps/add", methods=["GET", "POST"])
def add_app():
    form = EcobeeAppForm()
    if form.validate_on_submit():
        name = request.form["name"]
        api_key = request.form["api_key"]
        authorization_code = request.form["authorization_code"]
        access_token = request.form["access_token"]
        refresh_token = request.form["refresh_token"]
        app = Ecobee_API(name=name, api_key=api_key, authorization_code=authorization_code, access_token=access_token, refresh_token=refresh_token)
        if app.isAuthentic():
            app = apis(
                name=name,
                api_key=api_key,
                authorization_code=authorization_code,
                access_token=access_token,
                refresh_token=refresh_token,
            )
            db.session.add(app)
            db.session.commit()
            return redirect(url_for("apps_blueprint.home"))
        else:
            flash('App is not valid.', 'danger')
            return redirect(url_for('apps_blueprint.add_app'))
    return render_template("apps/components/add-app.html", form=form)


@apps_blueprint.route("/apps/<string:name>/delete", methods=["POST"])
def delete_app(name):
    app = apis.query.filter_by(name=name).first()
    db.session.delete(app)
    db.session.commit()
    return redirect(url_for("apps_blueprint.apps"))


# Thermostats


@apps_blueprint.route("/apps/<string:app_name>/")
@apps_blueprint.route("/apps/<string:app_name>/thermostats/")
def thermostats(app_name):
    app_config = apis.query.filter_by(name=app_name).first()
    app = Ecobee_API(config=app_config)
    thermostats = app.get_thermostats()
    if app.isAuthentic():
        return render_template("thermostats/view.html", app=app, thermostats=thermostats)
    else:
        flash('App is not valid.', 'danger')
        return redirect(url_for('apps_blueprint.apps'))


@apps_blueprint.route(
    "/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/",
    methods=["GET", "POST"],
)
def thermostat(app_name, thermostat_identifier):
    app_config = apis.query.filter_by(name=app_name).first()
    app = Ecobee_API(config=app_config)
    thermostats = app.get_thermostats()
    thermostat = [
        thermostat
        for thermostat in thermostats
        if thermostat.identifier == thermostat_identifier
    ][0]
    categories, series = get_graph_data(app)
    chartID = 'chart_ID'
    chart_type = 'spline'
    chart = {"renderTo": chartID, "type": chart_type}
    title = {"text": 'Thermostat'}
    xAxis = {"categories": categories}
    yAxis = {"title": {"text": 'Temperature'}}
    return render_template(
        "thermostats/thermostat/view.html",
        app_name=app_name,
        app=app,
        thermostat=thermostat,
        temperature_options=temperature_options,
        chartID=chartID,
        chart=chart,
        series=series,
        title=title,
        xAxis=xAxis,
        yAxis=yAxis
    )


# Thermostat Functions


@apps_blueprint.route(
    "/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/resume",
    methods=["POST"],
)
def resume(app_name, thermostat_identifier):
    app_config = apis.query.filter_by(name=app_name).first()
    app = Ecobee_API(config=app_config)
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
    app_config = apis.query.filter_by(name=app_name).first()
    app = Ecobee_API(config=app_config)
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
    app_config = apis.query.filter_by(name=app_name).first()
    app = Ecobee_API(config=app_config)
    message = request.form["message"]
    app.send_message(identifier=thermostat_identifier, message=message)
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
    app_config = apis.query.filter_by(name=app_name).first()
    app = Ecobee_API(config=app_config)
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
    app_config = apis.query.filter_by(name=app_name).first()
    app = Ecobee_API(config=app_config)
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
