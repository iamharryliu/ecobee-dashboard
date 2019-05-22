from flask import Blueprint
from ecobee import db
from ecobee.main.utils import Ecobee_API
from ecobee.main.models import apis


api = Blueprint("api", __name__, template_folder="templates")


@main.route(
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
    return render_template(
        "thermostats/thermostat/view.html",
        app_name=app_name,
        app=app,
        thermostat=thermostat,
        temperature_options=temperature_options,
    )
