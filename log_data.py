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
from pytz import timezone


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def push_app_context():
    flask_app = create_app()
    with flask_app.app_context() as ctx:
        ctx.push()


def get_timestamp():
    tz = timezone('EST')
    timestamp = datetime.now(tz)
    timestamp = timestamp.strftime('%m-%d-%y %H:%M')
    return timestamp


def log():
    timestamp = get_timestamp()
    push_app_context()
    apps = apis.query.all()
    for config in apps:
        app = Ecobee_API(config=config)
        thermostats = app.get_thermostats()

        for thermostat in thermostats:
            temperature = thermostat.temperature
            set_temperature = thermostat.current_climate_data.temperature
            occupancy = thermostat.sensor.occupancy
            humidity = thermostat.sensor.humidity
            fields = [timestamp, temperature, set_temperature, occupancy, humidity]
            with open(f'{DIR_PATH}/ecobee/logs/{app.api_key}-{thermostat.identifier}-{thermostat.sensor.id[0:2] + thermostat.sensor.id[-1:]}', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)

            for sensor in thermostat.remote_sensors:
                temperature = sensor.temperature
                occupancy = sensor.occupancy
                fields = [timestamp, temperature, set_temperature, occupancy]
                with open(f'{DIR_PATH}/ecobee/logs/{app.api_key}-{thermostat.identifier}-{sensor.id[0:2] + sensor.id[-3:]}', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)


if __name__ == '__main__':
    log()
