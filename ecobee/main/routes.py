from flask import Blueprint, render_template, redirect, url_for, flash, request
from ecobee import db
from ecobee.utils import Ecobee_API

main = Blueprint('main', __name__)

temperature_options = [n*0.5+18 for n in range(17)]

class ecobee_api_configs(db.Model):
	name = db.Column(db.String(20), unique=True)
	api_key = db.Column(db.String(32), primary_key=True)
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

@main.route('/apps/<string:app_name>/')
@main.route('/apps/<string:app_name>/thermostats/')
def thermostats(app_name):
	app_config = ecobee_api_configs.query.filter_by(name=app_name).first()
	app = Ecobee_API(config = app_config)
	thermostats = app.get_thermostats()
	return render_template('thermostats.html', app=app, thermostats=thermostats)

@main.route('/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/', methods=['GET', 'POST'])
def thermostat(app_name, thermostat_identifier):
	app_config = ecobee_api_configs.query.filter_by(name=app_name).first()
	app = Ecobee_API(config = app_config)
	thermostats = app.get_thermostats()
	thermostat = [thermostat for thermostat in thermostats if thermostat.identifier==thermostat_identifier][0]
	return render_template('thermostat.html', app_name=app_name, thermostat=thermostat, temperature_options=temperature_options)

@main.route('/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/resume', methods=['POST'])
def resume(app_name, thermostat_identifier):
	app_config = ecobee_api_configs.query.filter_by(name=app_name).first()
	app = Ecobee_API(config = app_config)
	app.resume(identifier=thermostat_identifier)
	return redirect(url_for('main.thermostat', app_name=app_name, thermostat_identifier=thermostat_identifier))

@main.route('/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/set_hvac_mode', methods=['POST'])
def set_hvac_mode(app_name, thermostat_identifier):
	app_config = ecobee_api_configs.query.filter_by(name=app_name).first()
	app = Ecobee_API(config = app_config)
	hvac_mode = request.form['hvac_mode']
	app.set_hvac_mode(identifier=thermostat_identifier, hvac_mode=hvac_mode)
	return redirect(url_for('main.thermostat', app_name=app_name, thermostat_identifier=thermostat_identifier))

@main.route('/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/send_message', methods=['POST'])
def send_message(app_name, thermostat_identifier):
	app_config = ecobee_api_configs.query.filter_by(name=app_name).first()
	app = Ecobee_API(config = app_config)
	message = request.form['message']
	app.send_message(identifier=thermostat_identifier, message=message)
	return redirect(url_for('main.thermostat', app_name=app_name, thermostat_identifier=thermostat_identifier))

@main.route('/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/set_climate_hold', methods=['POST'])
def set_climate_hold(app_name, thermostat_identifier):
	app_config = ecobee_api_configs.query.filter_by(name=app_name).first()
	app = Ecobee_API(config = app_config)
	climate = request.form['climate']
	app.set_climate_hold(identifier=thermostat_identifier, climate=climate)
	return redirect(url_for('main.thermostat', app_name=app_name, thermostat_identifier=thermostat_identifier))

@main.route('/apps/<string:app_name>/thermostats/<string:thermostat_identifier>/set_temperature_hold', methods=['POST'])
def set_temperature_hold(app_name, thermostat_identifier):
	app_config = ecobee_api_configs.query.filter_by(name=app_name).first()
	app = Ecobee_API(config = app_config)
	temperature = request.form['temperature']
	temperature = float(temperature)
	app.set_temperature_hold(identifier=thermostat_identifier, temperature=temperature)
	return redirect(url_for('main.thermostat', app_name=app_name, thermostat_identifier=thermostat_identifier))