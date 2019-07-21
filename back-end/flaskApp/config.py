import os
import json

import logging

# Database path to main directory to work with Flask-Migrate and SQLite.
# DIR_PATH = os.path.dirname(os.path.realpath(__file__))
# PARENT_PATH = os.path.abspath(os.path.join(DIR_PATH, os.pardir))

from pathlib import Path
home_dir = str(Path.home())

class Config:
    SECRET_KEY = "secret"
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///{PARENT_PATH}/site.db"
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/ecobee'
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/ecobee"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

ecobeeAppLogger = logging.getLogger(__name__)
ecobeeAppLogger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler(f"{home_dir}/logs/ecobeeApp.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
ecobeeAppLogger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
ecobeeAppLogger.addHandler(stream_handler)

temp_log_dir = f"{home_dir}/logs/ecobee_data/temp_and_humidity"
occupancy_log_dir = f"{home_dir}/logs/ecobee_data/occupancy"

# 18 to 26 degrees celsius, incrementing by .5
TEMPERATURE_OPTIONS = [n * 0.5 + 18 for n in range(17)]
# Span of hours that you want shown on the thermostat occupancy chart.
OCCUPANCY_HOURS = 24
