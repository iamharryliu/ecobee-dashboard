import os

# Database path to main directory to work with Flask-Migrate and SQLite.
# DIR_PATH = os.path.dirname(os.path.realpath(__file__))
# PARENT_PATH = os.path.abspath(os.path.join(DIR_PATH, os.pardir))


class Config:
    SECRET_KEY = "secret"
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///{PARENT_PATH}/site.db"
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/ecobee'
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/ecobee"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


import logging
from pathlib import Path

home_dir = str(Path.home())
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
