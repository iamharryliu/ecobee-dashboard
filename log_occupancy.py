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
log_dir = f'{home_dir}/logs/ecobee_data/occupancy'


def main():
    set_global_timestamp()
    push_app_context()
    apps = apis.query.all()
    for config in apps:
        handle_app(config)


def set_global_timestamp():
    ''' Set global timestamp. '''
    global timestamp
    timestamp = datetime.now()
    timestamp = timestamp.isoformat()


def handle_app(config):
    ''' Handle app. '''
    global app
    app = Ecobee_API(config=config)
    thermostats = app.get_thermostats()
    for thermostat in thermostats:
        handle_thermostat(thermostat)


def handle_thermostat(thermostat):
    ''' Handle thermostat '''
    global occupancy_path
    occupancy_path = f'{log_dir}/{app.api_key}-{thermostat.identifier}'
    global sensor_id_as_valid_filename

    # log_thermostat_temperature_data(thermostat)
    sensor = thermostat.sensor
    sensor_id_as_valid_filename = get_sensor_id_as_valid_filename(sensor)
    occupancy = sensor.occupancy
    log_sensor_occupancy(sensor)

    for sensor in thermostat.remote_sensors:
        sensor_id_as_valid_filename = get_sensor_id_as_valid_filename(sensor)
        occupancy = sensor.occupancy
        log_sensor_occupancy(sensor)


def log_sensor_occupancy(sensor):
    filepath = f'{occupancy_path}-{sensor_id_as_valid_filename}'
    # file_is_empty = os.stat(filepath).st_size == 0
    file_exists = os.path.isfile(filepath)
    file_does_not_exist = not (file_exists)
    occupancy_data = []

    # Control variable
    # sensor.occupancy = True

    if sensor.occupancy:
        if file_does_not_exist:
            fields = [timestamp, None]
            write_to_csv(filepath, fields)
        else:
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                for line in reader:
                    occupancy_data.append(line)
            recently_occupied = True if occupancy_data[-1][1] == '' else False
            if not recently_occupied:
                fields = [timestamp, None]
                write_to_csv(filepath, fields)
    else:
        if file_exists:
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                for line in reader:
                    occupancy_data.append(line)
            recently_occupied = True if occupancy_data[-1][1] == '' else False
            if recently_occupied:
                occupancy_data[-1][1] = timestamp
            with open(filepath, 'w') as f:
                writer = csv.writer(f)
                for line in occupancy_data:
                    writer.writerow(line)

        # print(sensor.id, 'not occupied')


def push_app_context():
    ''' Push app context. '''
    flask_app = create_app()
    with flask_app.app_context() as ctx:
        ctx.push()


def log_thermostat_temperature_data(thermostat):
    ''' Log thermostat temperature data (timestamp, actual temperature, set temperature) '''
    actual_temperature = thermostat.temperature
    set_temperature = thermostat.current_climate_data.temperature
    fields = [timestamp, actual_temperature, set_temperature]
    filepath = temperature_path
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
