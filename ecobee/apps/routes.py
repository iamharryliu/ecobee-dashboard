from flask import Blueprint, render_template, redirect, url_for, flash, request
from ecobee import db
from ecobee.models import apis
from ecobee.apps.utils import Ecobee_API, TEMPERATURE_OPTIONS
from ecobee.apps.forms import EcobeeAppForm

apps_blueprint = Blueprint("apps_blueprint", __name__, template_folder='templates')


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
            return redirect(url_for("main.home"))
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

    # Get app.
    app_config = apis.query.filter_by(name=app_name).first()
    app = Ecobee_API(config=app_config)

    # Get thermostat.
    thermostat = app.get_thermostat(thermostat_identifier)
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
