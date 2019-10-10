import os

# Database path to main directory to work with Flask-Migrate and SQLite.
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PARENT_PATH = os.path.abspath(os.path.join(DIR_PATH, os.pardir))


class Config:
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{PARENT_PATH}/site.db"
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/ecobee'
    # SQLALCHEMY_DATABASE_URI = "postgresql://localhost/ecobee"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True