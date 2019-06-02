# from ecobee.apps.utils import Ecobee_API
# import sqlite3
# conn = sqlite3.connect('site.db')
# c = conn.cursor()
# apis = c.execute("SELECT * FROM 'apis'")
from ecobee import create_app
from ecobee.models import apis
from ecobee.apps.utils import Ecobee_API
import os
import csv
from datetime import datetime
import re
from pathlib import Path

home_dir = str(Path.home())
log_dir = f'{home_dir}/logs/ecobee_data/temp_and_humidity'

timestamp = datetime.now()
timestamp = timestamp.isoformat()


def main():
    push_app_context()
    apps = apis.query.all()
    for config in apps:
        handle_app(config)


def handle_app(config):
    ''' Handle app. '''
    global app
    app = Ecobee_API(config=config)
    thermostats = app.get_thermostats()
    for thermostat in thermostats:
        handle_thermostat(thermostat)


def handle_thermostat(thermostat):
    ''' Handle thermostat '''

    global log_path
    log_path = f'{log_dir}/{app.api_key}-{thermostat.identifier}'
    global sensor_id_as_valid_filename

    print(log_path)

    log_thermostat_temperature_data(thermostat)
    sensor = thermostat.sensor
    sensor_id_as_valid_filename = get_sensor_id_as_valid_filename(sensor)
    log_sensor_temperature_and_humidity(sensor)

    for sensor in thermostat.remote_sensors:
        sensor_id_as_valid_filename = get_sensor_id_as_valid_filename(sensor)
        log_sensor_temperature_and_humidity(sensor)


def push_app_context():
    ''' Push app context. '''
    flask_app = create_app()
    with flask_app.app_context() as ctx:
        ctx.push()


def log_thermostat_temperature_data(thermostat):
    ''' Log thermostat temperature data (timestamp, actual temperature, set temperature) '''
    actual_temperature = thermostat.actual_temperature
    set_temperature = thermostat.current_climate_data.temperature
    fields = [timestamp, actual_temperature, set_temperature]
    filepath = log_path
    write_to_csv(filepath, fields)


def log_sensor_temperature_and_humidity(sensor):
    ''' Log sensor data (timestamp, temperature) '''
    temperature = sensor.temperature
    try:
        humidity = sensor.humidity
    except Exception as e:
        print(e)
        humidity = None
    fields = [timestamp, temperature, humidity]
    filepath = f'{log_path}-{sensor_id_as_valid_filename}'
    write_to_csv(filepath, fields)


def get_sensor_id_as_valid_filename(sensor):
    ''' Used to get a sensor name that could be saved as a file. ei:0 -> ei0'''
    r = re.compile(r'[^a-z0-9]')
    sensor_id_as_valid_filename = r.sub('', sensor.id)
    return sensor_id_as_valid_filename


def write_to_csv(filepath, fields):
    ''' Write data to csv fields to csv file. '''
    with open(filepath, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)


if __name__ == '__main__':
    main()
