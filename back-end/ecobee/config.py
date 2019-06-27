import os
import json

import logging
from pathlib import Path

# Database path to be in the main directory to work with Flask-Migrate.
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PARENT_PATH = os.path.abspath(os.path.join(DIR_PATH, os.pardir))


class Config:
    SECRET_KEY = "secret"
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///{PARENT_PATH}/site.db"
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/ecobee'
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/ecobee"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    # CORS_HEADERS = 'Content-Type'


logger = logging.getLogger(__name__)
home_dir = str(Path.home())
file_handler = logging.FileHandler(f'{home_dir}/logs/ecobee_dash.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

temp_log_dir = f'{home_dir}/logs/ecobee_data/temp_and_humidity'
occupancy_log_dir = f'{home_dir}/logs/ecobee_data/occupancy'

TEMPERATURE_OPTIONS = [n * 0.5 + 18 for n in range(17)]  # 18 to 26 degrees celsius, incrementing by .5
OCCUPANCY_HOURS = 24  # Span of time that you want shown on the thermostat occupancy chart.
