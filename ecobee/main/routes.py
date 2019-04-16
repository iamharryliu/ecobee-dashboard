from flask import Blueprint, render_template, redirect, url_for, flash, request
from ecobee import db
from ecobee.main.utils import Ecobee_API
from ecobee.main.models import ecobee_api_configs
from ecobee.main.forms import EcobeeAppForm


main = Blueprint('main', __name__, template_folder='templates')

temperature_options = [n*0.5+18 for n in range(17)]

@main.route('/')
def home():
	return render_template('main.html')

@main.route('/apps/add', methods=['GET','POST'])
def add_app():
	form = EcobeeAppForm()
	if form.validate_on_submit():
		name = request.form['name']
		api_key = request.form['api_key']
		authorization_code = request.form['authorization_code']
		access_token = request.form['access_token']
		refresh_token = request.form['refresh_token']
		app = ecobee_api_configs(name=name, api_key=api_key, authorization_code=authorization_code,
			access_token=access_token, refresh_token=refresh_token)
		db.session.add(app)
		db.session.commit()
		return redirect(url_for('main.home'))
	return render_template('add_app.html', form=form)

@main.route('/apps/<string:name>/delete', methods=['POST'])
def delete_app(name):
	app = ecobee_api_configs.query.filter_by(name=name).first()
	db.session.delete(app)
	db.session.commit()
	return redirect(url_for('main.apps'))

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