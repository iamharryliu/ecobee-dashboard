import os
import json

# We want the database path to be in the main directory to work with Flask-Migrate.
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))


class Config:
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{parent_path}/site.db"
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/ecobee'
    # SQLALCHEMY_DATABASE_URI = "postgresql://localhost/ecobee"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
