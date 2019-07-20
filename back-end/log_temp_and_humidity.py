from ecobee import create_app
from ecobee.models import App
from ecobeeAPI import EcobeeAPI
from ecobee.apps.utils import getThermostats

import os
from pathlib import Path
import re
import csv

from datetime import datetime

home_dir = str(Path.home())
log_dir = f"{home_dir}/logs/ecobee_data/temp_and_humidity"

timestamp = datetime.now()
timestamp = timestamp.isoformat()


def main():
    push_app_context()
    apps = App.query.all()
    for config in apps:
        handle_app(config)


def push_app_context():
    """ Push app context. """
    flask_app = create_app()
    with flask_app.app_context() as ctx:
        ctx.push()


def handle_app(config):
    """ Handle app. """
    global app
    app = EcobeeAPI(config=config)
    thermostats = getThermostats(app)
    for thermostat in thermostats:
        handle_thermostat(thermostat)


def handle_thermostat(thermostat):
    """ Handle thermostat """

    global log_path
    log_path = f"{log_dir}/{app.api_key}-{thermostat.identifier}"
    global sensor_id_as_valid_filename

    log_thermostat_temperature_data(thermostat)

    sensor = thermostat.sensor
    sensor_id_as_valid_filename = get_sensor_id_as_valid_filename(sensor)
    log_sensor_temperature_and_humidity(sensor)

    for sensor in thermostat.remote_sensors:
        sensor_id_as_valid_filename = get_sensor_id_as_valid_filename(sensor)
        log_sensor_temperature_and_humidity(sensor)


def log_thermostat_temperature_data(thermostat):
    """ Log thermostat temperature data (timestamp, actual temperature, set temperature) """
    actual_temperature = thermostat.actual_temperature
    set_temperature = thermostat.current_climate_data.temperature
    fields = [timestamp, actual_temperature, set_temperature]
    filepath = log_path
    write_to_csv(filepath, fields)


def log_sensor_temperature_and_humidity(sensor):
    """ Log sensor data (timestamp, temperature) """
    temperature = sensor.temperature
    try:
        humidity = sensor.humidity
    except:
        humidity = None
    fields = [timestamp, temperature, humidity]
    filepath = f"{log_path}-{sensor_id_as_valid_filename}"
    write_to_csv(filepath, fields)


def get_sensor_id_as_valid_filename(sensor):
    """ Used to get a sensor name that could be saved as a file. ei:0 -> ei0"""
    r = re.compile(r"[^a-z0-9]")
    sensor_id_as_valid_filename = r.sub("", sensor.id)
    return sensor_id_as_valid_filename


def write_to_csv(filepath, fields):
    """ Write data to csv fields to csv file. """
    with open(filepath, "a") as f:
        writer = csv.writer(f)
        writer.writerow(fields)


if __name__ == "__main__":
    main()
