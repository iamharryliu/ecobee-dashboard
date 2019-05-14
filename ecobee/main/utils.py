import requests, json, logging
from flask import flash

from ecobee import db

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('eobee_api.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

ecobee_url = 'https://api.ecobee.com/'

class Ecobee_API():
	def __init__(self, config=None, name=None, api_key=None, authorization_code=None, access_token=None, refresh_token=None):
		if config:
			self.config = config
			self.name = config.name
			self.api_key = config.api_key
			self.authorization_code = config.authorization_code
			self.access_token = config.access_token
			self.refresh_token = config.refresh_token
		else:
			self.name = name
			self.api_key = api_key
			self.authorization_code = authorization_code
			self.access_token = access_token
			self.refresh_token = refresh_token

	def request_pin(self):
		logger.info(f'Attempting to request pin for {self.api_key}')
		url = f'{ecobee_url}authorize'
		params = {
			'response_type': 'ecobeePin',
			'client_id': self.api_key, 
			'scope': 'smartWrite'
		}
		try:
			request = requests.get(url, params=params)
		except RequestException:
			logger.warn(f'Pin request for {self.api_key} unsuccessful')
		else:
			if request.status_code == requests.codes.ok:
				logger.info(f'Pin request for {self.api_key} successful')
				self.authorization_code = request.json()['code']
				self.pin = request.json()['ecobeePin']
			else:
				return False

	def request_tokens(self):
		logger.info(f'Attempting to request tokens for {self.api_key}')
		url = f'{ecobee_url}token'
		params = {'grant_type': 'ecobeePin', 'code': self.authorization_code,
		'client_id': self.api_key}
		try:
			request = requests.post(url, params=params)
		except RequestException:
			return
		else:
			if request.status_code == requests.codes.ok:
				logger.info(f'Tokens request for {self.api_key} successful')
				self.access_token = request.json()['access_token']
				self.refresh_token = request.json()['refresh_token']
				self.write_to_db()
				self.pin = None
			else:
				logger.info(f'Tokens request for {self.api_key} unsuccessful')
				return

	def make_request(self, body, log_msg_action):
			url = f'{ecobee_url}1/thermostat'
			header = {
				'Content-Type': 'application/json;charset=UTF-8',
				'Authorization': 'Bearer ' + self.access_token
			}
			params = {
				'format': 'json'
			}
			try:
				logger.info(f'Thermostat Action request for {self.api_key} successful:\n\t{log_msg_action}')
				request = requests.post(url, headers=header, params=params, json=body)
			except RequestException:
				logger.warn(f'Thermostat Action request for {self.api_key} unsuccessful:\n\t{log_msg_action}')
				return False
			else:
				if request.status_code == requests.codes.ok:
					return True
				else:
					if self.refresh_tokens():
						return self.make_request(body, log_msg_action)
					else:
						return False


	def refresh_tokens(self):
		logger.info(f'Attempting to refresh tokens for {self.api_key}')
		url = f'{ecobee_url}token'
		params = {
			'grant_type': 'refresh_token',
			'refresh_token': self.refresh_token,
			'client_id': self.api_key
		}
		request = requests.post(url, params=params)
		if request.status_code == requests.codes.ok:
			logger.info(f'Refresh token request for {self.api_key} successful')
			self.access_token = request.json()['access_token']
			self.refresh_token = request.json()['refresh_token']
			self.write_to_db()
			return True
		else:
			logger.warn(f'Refresh token request for {self.api_key} unsuccessful')
			self.request_pin()



	def write_to_db(self):
		logger.info(f'Writing {self.api_key} data to db')
		self.config.api_key = self.api_key
		self.config.authorization_code = self.authorization_code
		self.config.access_token = self.access_token
		self.config.refresh_token = self.refresh_token
		db.session.commit()

	def isAuthentic(self, refreshed=False):
		url = f'{ecobee_url}1/thermostat'
		header = {'Content-Type': 'application/json;charset=UTF-8',\
                  'Authorization': 'Bearer ' + self.access_token}
		params = {
					'json': (
						'''{\
							"selection":{\
								"selectionType":"registered"
						}\
					}'''
				)
		}
		try:
			request = requests.get(url, headers=header, params=params)
		except:
			pass
			# logger.warn(f'Request for {self.api_key} unsuccessful.')
		else:
			if request.status_code == requests.codes.ok:
				# logger.info(f'Request for {self.api_key} successful')
				return True
			else:
				if self.refresh_tokens():
					return self.isAuthentic(refreshed=True)
				else:
					return False
	
	def get_json(self):
		logger.info(f'Attempting to get json data for {self.api_key}')
		url = f'{ecobee_url}1/thermostat'
		header = {'Content-Type': 'application/json;charset=UTF-8',\
                  'Authorization': 'Bearer ' + self.access_token}
		params = {
					'json': (
						'''{\
							"selection":{\
								"selectionType":"registered",\
								"includeRuntime":"true",\
								"includeSensors":"true",\
								"includeProgram":"true",\
								"includeEquipmentStatus":"true",\
								"includeEvents":"true",\
								"includeWeather":"true",\
								"includeSettings":"true"\
						}\
					}'''
				)
		}
		try:
			request = requests.get(url, headers=header, params=params)
		except:
			logger.warn(f'JSON request for {self.api_key} unsuccessful.')
		else:
			if request.status_code == requests.codes.ok:
				logger.info(f'JSON request for {self.api_key} successful')
				thermostats = request.json()['thermostatList']
				return thermostats
			else:
				if self.refresh_tokens():
					return self.get_json()
				else:
					return []

	def resume(self, identifier, resume_all=False):
		body = {"selection": 
					{ 
						"selectionType": "thermostats", 
						"selectionMatch": identifier
					}, 
					"functions": [ 
						{ 
							"type": "resumeProgram", 
							"params": { 
							"resumeAll": resume_all 
							} 
						} 
					] 
				}
		log_msg_action = f'Thermostat: {identifier} program resumed'
		return self.make_request(body, log_msg_action)

	def set_hvac_mode(self, identifier, hvac_mode):
		body = {
			"selection": {
				"selectionType": "thermostats",
				"selectionMatch": identifier
			},
			"thermostat": {
				"settings": {
					"hvacMode": hvac_mode
				}
			}
		}
		log_msg_action = f'Thermostat: {identifier} HVAC mode set to {hvac_mode}'
		return self.make_request(body, log_msg_action)
		
	def set_temperature_hold(self, identifier, temperature, hold_type="holdHours", holdHours=2):
		temperature = degreees_to_farenheit(temperature)
		body = {"selection": 
			{
				"selectionType": "thermostats",
				"selectionMatch": identifier
			},
			"functions": [
				{
					"type": "setHold",
					"params": {
						"holdType": hold_type,
						"coolHoldTemp": int(temperature),
						"heatHoldTemp": int(temperature),
						"holdHours": holdHours
					}
				}
			]
		}
		log_msg_action = f"Themrostat: {identifier} set to hold {temperature}"
		return self.make_request(body, log_msg_action)

	def set_climate_hold(self, identifier, climate, hold_type="nextTransition"):
		body = {
			"selection": {
				"selectionType": "thermostats",
				"selectionMatch": identifier
			 },
			"functions": [
				{
					"type": "setHold", "params": 
						{
							"holdType": hold_type,
							"holdClimateRef": climate
						}
				}
			]
		}
		log_msg_action = f"Thermostat: {identifier} set to hold {climate} climate"
		return self.make_request(body, log_msg_action)

	def send_message(self, identifier, message="Hello world!"):
		body = {
			"selection": {
				"selectionType": "thermostats",
				"selectionMatch": identifier
			},
			"functions": [
				{
					"type": "sendMessage",
					"params": {
						"text": message[0:500]
					}
				}
			]
		}

		log_msg_action = f"Send Message: {message}"
		return self.make_request(body, log_msg_action)

	def create_vacation(self, identifier, vacation):
		body = {
			"selection": {
				"selectionType": "thermostats",
				"selectionMatch": identifier
			},
			"functions": [
				{
				"type":"createVacation",
					"params":{
						"name": vacation.name,
						"coolHoldTemp": vacation.temperature,
						"heatHoldTemp": vacation.temperature,
						"startDate": vacation.start_date,
						"startTime": vacation.start_time,
						"endDate": vacation.end_date,
						"endTime": vacation.end_time
					}
				}
			]
		}
		log_msg_action = f"Thermostat: {idenfifier} add vacation ({name} / {vacation.temperature} / {vacation.start_time} {vacation.end_time} to {vacation.end_date} {vacation.end_time})"
		return self.make_request(body, log_msg_action)                     

	def get_thermostats(self):
		thermostats = []
		thermostats_json = self.get_json()
		for thermostat_json in thermostats_json:

			thermostat = Thermostat(thermostat_json)

			thermostats.append(thermostat)

		return thermostats

class Thermostat():
	def __init__(self, thermostat):	
		self.set_thermostat(thermostat)

	def set_thermostat(self, thermostat):
		self.identifier = thermostat['identifier']
		self.name = thermostat['name']
		self.hvac_mode = thermostat['settings']['hvacMode']
		self.temperature = self.get_temperature(thermostat)
		self.climates = self.get_climates(thermostat)
		self.remote_sensors = self.get_remote_sensors(thermostat)
		self.sensor = self.get_thermostat_sensor(thermostat)
		self.current_climate_data = self.get_current_climate_data(thermostat)

	def get_current_climate_data(self, thermostat):
		return CurrentClimateData(thermostat)

	def get_climates(self,thermostat):
		climates = []
		for climate in thermostat['program']['climates']:
			climates.append(climate['climateRef'])
		return climates

	def get_thermostat_sensor(self, thermostat):
		sensors_json = thermostat['remoteSensors']
		gen = (sensor_json for sensor_json in sensors_json if sensor_json['type'] != 'ecobee3_remote_sensor')
		for sensor_json in gen:
			sensor = ThermostatSensor(sensor_json)
		return sensor

	def get_remote_sensors(self, thermostat):
		sensors = []
		sensors_json = thermostat['remoteSensors']
		gen = (sensor_json for sensor_json in sensors_json if sensor_json['type'] == 'ecobee3_remote_sensor')
		for sensor_json in gen:
			sensor = RemoteSensor(sensor_json)
			sensors.append(sensor)
		return sensors

	def get_temperature(self, thermostat):
		temperature = thermostat['runtime']['actualTemperature']
		temperature = farenheit_to_degrees(temperature)
		return temperature

class RemoteSensor():
	def __init__(self, sensor):
		self.name = sensor['name']
		self.type = sensor['type']
		self.code = sensor['code']
		self.humidity = 'n/a'
		self.occupancy = sensor['capability'][1]['value']
		temperature = sensor['capability'][0]['value']
		if temperature != 'unknown':
			self.active = True
			temperature = float(temperature)
			self.temperature = farenheit_to_degrees(temperature)
		else:
			self.active = False
			self.temperature = None

class ThermostatSensor():
	def __init__(self, sensor):
		self.name = sensor['name']
		self.type = sensor['type']
		self.code = 'n/a'
		self.humidity = sensor['capability'][1]['value']
		self.occupancy = sensor['capability'][2]['value']
		self.active = True
		temperature = sensor['capability'][0]['value']
		if temperature != 'unknown':
			self.active = True
			temperature = float(temperature)
			self.temperature = farenheit_to_degrees(temperature)
		else:
			self.active = False
			self.temperature = None

class CurrentClimateData():
	def __init__(self, thermostat):
		if thermostat['events']:
			self.events = True
			holdClimateRef = thermostat['events'][0]['holdClimateRef']
			if holdClimateRef == "":
				self.mode = 'hold'
				temperature = thermostat['events'][0]['heatHoldTemp']
				self.temperature =farenheit_to_degrees(temperature)
			else:
				self.mode = holdClimateRef
				for climate in thermostat['program']['climates']:
					if self.mode == climate['climateRef']:
						temperature =  climate['heatTemp']
						self.temperature = farenheit_to_degrees(temperature)
			self.end_date = thermostat['events'][0]['endDate']
			self.end_time = thermostat['events'][0]['endTime']
		else:
			self.events = False
			self.mode = thermostat['program']['currentClimateRef']
			for climate in thermostat['program']['climates']:
				if self.mode == climate['climateRef']:
					temperature = climate['heatTemp']
					self.temperature = farenheit_to_degrees(temperature)
			self.end_date = 'transition'
			self.end_time = 'transition'


def farenheit_to_degrees(temperature):
	temperature = (temperature - 320) * 5 / 90
	temperature = round(temperature,2)
	return temperature

def degreees_to_farenheit(temperature):
	temperature = temperature * 90 / 5 + 320
	temperature = round(temperature,2)
	return temperature