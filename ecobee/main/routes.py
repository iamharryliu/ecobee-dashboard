from flask import Blueprint, render_template, redirect, url_for, flash
from ecobee import db
from ecobee.utils import Ecobee_API

main = Blueprint('main', __name__)

class ecobee_api_configs(db.Model):
	api_key = db.Column(db.String(32), primary_key=True)
	name = db.Column(db.String(20))
	authorization_code = db.Column(db.String(32), nullable=False)
	access_token = db.Column(db.String(32), nullable=False)
	refresh_token = db.Column(db.String(32), nullable=False)

@main.route('/')
def home():
	return render_template('main.html')

@main.route('/apps/')
def apps():
	apps = ecobee_api_configs.query.all()
	return render_template('apps.html', apps=apps)

@main.route('/apps/<string:app_name>')
def thermostats(app_name):
	app_config = ecobee_api_configs.query.filter_by(name=app_name).first()
	app = Ecobee_API(config = app_config)
	thermostats = app.get_thermostats()

	return render_template('thermostats.html', app=app, thermostats=thermostats)

@main.route('/thermostat/')
def thermostat():
	return render_template('thermostat.html')