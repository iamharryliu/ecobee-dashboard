'''

logging

'''

import requests, json, logging

from ecobee import db


logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

ecobee_url = 'https://api.ecobee.com/'

class Ecobee_API():
	def __init__(self, config=None):
		
		if config:
			self.config = config
			self.name = config.name
			self.api_key = config.api_key
			self.authorization_code = config.authorization_code
			self.access_token = config.access_token
			self.refresh_token = config.refresh_token

	def get_json(self):
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
			pass
		if request.status_code == requests.codes.ok:
			print('REQUEST FOR THERMOSTATS: SUCCESS')
			thermostats = request.json()['thermostatList']
			return thermostats
		else:
			print('REQUEST FOR THERMOSTATS: FAIL')
			if self.refresh_tokens():
				return self.get_json()
			else:
				return

	def refresh_tokens(self):
		url = f'{ecobee_url}token'
		params = {
			'grant_type': 'refresh_token',
			'refresh_token': self.refresh_token,
			'client_id': self.api_key
		}
		request = requests.post(url, params=params)
		if request.status_code == requests.codes.ok:
			print('REQUEST TO REFRESH TOKENS: SUCCESS')
			self.access_token = request.json()['access_token']
			self.refresh_token = request.json()['refresh_token']
			self.write_to_db()
			return True
		else:
			print('REQUEST TO REFRESH TOKENS: FAIL')
			self.request_pin()


	def request_pin(self):
		url = f'{ecobee_url}authorize'
		params = {
			'response_type': 'ecobeePin',
			'client_id': self.api_key, 
			'scope': 'smartWrite'
		}
		try:
			request = requests.get(url, params=params)
		except RequestException:
			print('REQUEST FOR PIN: FAIL')
			return
		print('REQUEST FOR PIN: SUCCESS')
		self.authorization_code = request.json()['code']
		self.pin = request.json()['ecobeePin']
		print(f'\tAPI KEY: {self.api_key}')
		print(f'\tAUTHORIZATION CODE: {self.authorization_code}')
		print(f'\tPIN: {self.pin}')

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
			request = requests.post(url, headers=header, params=params, json=body)
		except RequestException:
			return None
		if request.status_code == requests.codes.ok:
			return True
		else:
			if self.refresh_tokens():
				return self.make_request(body, log_msg_action)
			else:
				return None

	def write_to_db(self):
		self.config.api_key = self.api_key
		self.config.authorization_code = self.authorization_code
		self.config.access_token = self.access_token
		self.config.refresh_token = self.refresh_token
		db.session.commit()
		
	def request_tokens(self):
		url = f'{ecobee_url}token'
		params = {'grant_type': 'ecobeePin', 'code': self.authorization_code,
		'client_id': self.api_key}
		try:
			request = requests.post(url, params=params)
		except RequestException:
			return
			if request.status_code == requests.codes.ok:
				self.access_token = request.json()['access_token']
				self.refresh_token = request.json()['refresh_token']
				self.write_to_db()
				self.pin = None
			else:
				return

	def get_temperature(self):
		temperature = self.thermostats[0]['runtime']['actualTemperature']
		temperature = (temperature - 320) * 5 / 90
		temperature = round(temperature,2)
		return temperature

	# Thermostat Actions

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
		print('resumed')	
		log_msg_action = "resume program"
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
		log_msg_action = "set HVAC mode"
		return self.make_request(body, log_msg_action)
		
	def set_temperature_hold(self, identifier, temperature, hold_type="holdHours", holdHours=2):
		print(f'temperature set to {temperature}')
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
		log_msg_action = "set hold temperature"
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
		log_msg_action = "set climate hold"
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

		log_msg_action = "send message"
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
			self.enddate = thermostat['events'][0]['endDate']
			self.endtime = thermostat['events'][0]['endTime']
		else:
			self.mode = thermostat['program']['currentClimateRef']
			for climate in thermostat['program']['climates']:
				if self.mode == climate['climateRef']:
					temperature = climate['heatTemp']
					self.temperature = farenheit_to_degrees(temperature)
			self.enddate = 'transition'
			self.endtime = 'transition'


def farenheit_to_degrees(temperature):
	temperature = (temperature - 320) * 5 / 90
	temperature = round(temperature,2)
	return temperature

def degreees_to_farenheit(temperature):
	temperature = temperature * 90 / 5 + 320
	temperature = round(temperature,2)
	return temperature