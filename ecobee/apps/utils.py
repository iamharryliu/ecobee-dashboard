import requests
import json
import logging
import csv
from flask import flash, request
from ecobee import db
from datetime import datetime, timedelta
import time

import dateutil.parser

from pathlib import Path
home_directory = str(Path.home())

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler(f'{home_directory}/logs/ecobee_dash.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# logger.setLevel(logging.DEBUG)
# logging.basicConfig(filename='ecobee_dash.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


temperature_options = [n * 0.5 + 18 for n in range(17)]

ecobee_url = 'https://api.ecobee.com/'

from pathlib import Path
home_dir = str(Path.home())
log_dir = f'{home_dir}/logs/ecobee_data/temp_and_humidity'

occupancy_log_dir = f'{home_dir}/logs/ecobee_data/occupancy'

dt_to_milliseconds = lambda dt: dt.timestamp() * 1000

today = datetime.now()
one_day = timedelta(days=1)
half_a_day = timedelta(hours=12)
half_a_day_ago = today - half_a_day
half_a_day_ago = dt_to_milliseconds(half_a_day_ago)
yesterday = today - one_day
yesterday = dt_to_milliseconds(yesterday)

class Ecobee_API():
    def __init__(self, config=None, name=None, api_key=None, authorization_code=None, access_token=None, refresh_token=None):
        if config:
            self.config = config
            self.name = config.name
            self.api_key = config.api_key
            self.authorization_code = config.authorization_code
            self.access_token = config.access_token
            self.refresh_token = config.refresh_token
            self.activate()
        else:
            self.name = name
            self.api_key = api_key
            self.authorization_code = authorization_code
            self.access_token = access_token
            self.refresh_token = refresh_token

    def __str__(self):
        return json.dumps(self.json, indent=2)

    def isAuthentic(self):
        url = f'{ecobee_url}1/thermostat'
        header = self.get_request_header()
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
            response = requests.get(url, headers=header, params=params)
        except:
            pass
            logger.warn(f'Request for {self.api_key} unsuccessful.')
        else:
            if response.status_code == requests.codes.ok:
                logger.info(f'Request for {self.api_key} successful')
                return True
            else:
                return False

    def activate(self):
        logger.info(f'Attempting to get json data for {self.api_key}')
        url = f'{ecobee_url}1/thermostat'
        header = self.get_request_header()
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
            response = requests.get(url, headers=header, params=params)
        except:
            logger.warn(f'JSON request for {self.api_key} unsuccessful.')
        else:
            if response.status_code == requests.codes.ok:
                logger.info(f'JSON request for {self.api_key} successful')
                self.json = json.loads(response.text)
            else:
                if self.refresh_tokens():
                    return self.activate()
                else:
                    return []

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
        except:
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
        params = {'grant_type': 'ecobeePin',
                  'code': self.authorization_code,
                  'client_id': self.api_key}
        try:
            request = requests.post(url, params=params)
        except:
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
        header = self.get_request_header()
        params = {
            'format': 'json'
        }
        try:
            logger.info(f'Thermostat Action request for {self.api_key} successful:\n\t{log_msg_action}')
            response = requests.post(url, headers=header, params=params, json=body)
        except:
            logger.warn(f'Thermostat Action request for {self.api_key} unsuccessful:\n\t{log_msg_action}')
            return False
        else:
            if response.status_code == requests.codes.ok:
                return True
            else:
                if self.refresh_tokens():
                    return self.make_request(body, log_msg_action)
                else:
                    return False

    def get_request_header(self):
        header = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': 'Bearer ' + self.access_token
        }
        return header

    def refresh_tokens(self):
        logger.info(f'Attempting to refresh tokens for {self.api_key}')
        url = f'{ecobee_url}token'
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.api_key
        }
        response = requests.post(url, params=params)
        if response.status_code == requests.codes.ok:
            logger.info(f'Refresh token request for {self.api_key} successful')
            self.access_token = response.json()['access_token']
            self.refresh_token = response.json()['refresh_token']
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

    def resume(self, identifier, resume_all=False):
        _type = "resumeProgram"
        params = {"resumeAll": resume_all}
        body = self.get_request_body(identifier, params=params, _type=_type)
        log_msg_action = f'Thermostat: {identifier} program resumed'
        return self.make_request(body, log_msg_action)

    def set_hvac_mode(self, identifier, hvac_mode):
        settings = {"hvacMode": hvac_mode}
        body = self.get_request_body(identifier, settings=settings)
        log_msg_action = f'Thermostat: {identifier} HVAC mode set to {hvac_mode}'
        return self.make_request(body, log_msg_action)

    def set_temperature_hold(self, identifier, temperature, hold_type="holdHours", holdHours=2):
        _type = "setHold"
        temperature = degreees_to_farenheit(temperature)
        params = {
            "holdType": hold_type,
            "coolHoldTemp": int(temperature),
            "heatHoldTemp": int(temperature),
            "holdHours": holdHours
        }
        body = self.get_request_body(identifier, params=params, _type=_type)
        log_msg_action = f"Themrostat: {identifier} set to hold {temperature}"
        return self.make_request(body, log_msg_action)

    def set_climate_hold(self, identifier, climate, hold_type="nextTransition"):
        _type = "setHold"
        params = {"holdType": hold_type, "holdClimateRef": climate}
        body = self.get_request_body(identifier, params=params, _type=_type)
        log_msg_action = f"Thermostat: {identifier} set to hold {climate} climate"
        return self.make_request(body, log_msg_action)

    def send_message(self, identifier, message="Hello world!"):
        _type = "sendMessage"
        params = {"text": message[0:500]}
        body = self.get_request_body(identifier, params=params, _type=_type)
        log_msg_action = f"Send Message: {message}"
        return self.make_request(body, log_msg_action)

    def create_vacation(self, identifier, vacation):
        _type = "createVacation"
        params = {
            "name": vacation.name,
            "coolHoldTemp": vacation.temperature,
            "heatHoldTemp": vacation.temperature,
            "startDate": vacation.start_date,
            "startTime": vacation.start_time,
            "endDate": vacation.end_date,
            "endTime": vacation.end_time
        }
        body = self.get_request_body(identifier, params=params, type=_type)

        log_msg_action = f"Thermostat: {idenfifier} add vacation ({name} / {vacation.temperature} / {vacation.start_time} {vacation.end_time} to {vacation.end_date} {vacation.end_time})"
        return self.make_request(body, log_msg_action)

    def get_thermostats(self):
        thermostats = []
        thermostats_json = self.json['thermostatList']
        for thermostat_json in thermostats_json:

            thermostat = Thermostat(thermostat_json)

            thermostats.append(thermostat)

        return thermostats

    def get_thermostat(self, identifier):
        self.thermostats = self.get_thermostats()
        thermostat = next(thermostat for thermostat in self.thermostats if thermostat.identifier == identifier)
        return thermostat

    def get_request_body(self, identifier, settings=None, params=None, _type=None):
        selection = self.request_body_selection(identifier)
        body = dict()
        body['selection'] = selection
        if params:
            function = dict()
            function['type'] = _type
            function['params'] = params
            functions = [function]
            body['functions'] = functions
        if settings:
            body['thermostat'] = dict()
            body['thermostat']['settings'] = settings
        return body

    def request_body_selection(self, identifier):
        selection = {
            "selectionType": "thermostats",
            "selectionMatch": identifier
        }
        return selection


class Thermostat():
    def __init__(self, thermostat):
        self.set_thermostat(thermostat)

    def set_thermostat(self, thermostat):
        self.identifier = thermostat['identifier']
        self.name = thermostat['name']
        self.hvac_mode = thermostat['settings']['hvacMode']
        self.actual_temperature = self.get_actual_temperature(thermostat)
        self.climates = self.get_climates(thermostat)
        self.remote_sensors = self.get_remote_sensors(thermostat)
        self.sensor = self.get_thermostat_sensor(thermostat)
        self.current_climate_data = self.get_current_climate_data(thermostat)

    def get_current_climate_data(self, thermostat):
        return CurrentClimateData(thermostat)

    def get_climates(self, thermostat):
        climates = []
        for climate in thermostat['program']['climates']:
            climates.append(ClimateObj(climate))

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

    def get_actual_temperature(self, thermostat):
        temperature = thermostat['runtime']['actualTemperature']
        temperature = farenheit_to_degrees(temperature)
        return temperature

    def get_temperature(self, thermostat):
        temperature = thermostat['remoteSensors'][-1]['capability'][0]['value']
        temperature = float(temperature)
        temperature = farenheit_to_degrees(temperature)
        return temperature

    def get_occupancy_chart_data(self, api_key):

        categories = None
        series = None

        categories = self.get_occupancy_chart_categories()
        series = self.get_occupancy_chart_series(api_key)

        chart_data = dict()
        chart_data['chart_id'] = 'occupancy_chart'
        chart_data['chart'] = {"type": 'xrange', 'styledMode': True, 'zoomType': 'x'}
        chart_data['title'] = {"text": 'Occupancy Chart'}
        chart_data['xAxis'] = {'type': 'datetime', 'min': half_a_day_ago, 'tickInterval': 1000* 60* 60, 'minorTicks':True, 'minorTickInterval': 1000*60*30, 'dateTimeLabelFormats':{'hour':'%l:%M %P'}}
        chart_data['yAxis'] = {"title": {"text": ''}, 'categories':categories, 'reversed':True}
        chart_data['series'] = series


        return chart_data

    def get_occupancy_chart_categories(self):
        categories = []
        categories.append('Thermostat')
        for sensor in self.remote_sensors:
            categories.append(sensor.name)
        return categories

    def get_occupancy_chart_series(self, api_key):
        series = []
        filename = f'{occupancy_log_dir}/{api_key}-{self.identifier}-ei0'
        series.append(self.get_thermostat_occupancy_set(api_key))
        sensor_sets = self.get_sensor_occupancy_sets(api_key)
        series += sensor_sets
        return series

    def get_thermostat_occupancy_set(self, api_key):
        filename = f'{occupancy_log_dir}/{api_key}-{self.identifier}-{self.sensor.file_id}'
        thermostat_set = dict()
        thermostat_set['name'] = 'Thermostat'
        # tehrmostart_set['pointPadding'] = 0
        thermostat_set['groupPadding'] = 0.5
        thermostat_set['pointWidth'] = 20
        thermostat_set['data_labels'] = {'enabled': False}
        set_data = []
        with open(filename) as f:
            reader = csv.reader(f)
            for line in reader:
                start = dateutil.parser.parse(line[0])
                start = dt_to_milliseconds(start)
                if line[1] == '':
                    end = datetime.now()
                    end = dt_to_milliseconds(end)
                else:
                    end = dateutil.parser.parse(line[1])
                    end = dt_to_milliseconds(end)
                data = {'x':start, 'x2':end, 'y':0}
                set_data.append(data)
        thermostat_set['data'] = set_data
        return thermostat_set

    def get_sensor_occupancy_sets(self, api_key):
        sets = []
        for index, sensor in enumerate(self.remote_sensors):
            try:
                filename = f'{occupancy_log_dir}/{api_key}-{self.identifier}-{sensor.file_id}'
                sensor_set = dict()
                sensor_set['name'] = sensor.name
                # tehrmostart_set['pointPadding'] = 0
                sensor_set['groupPadding'] = 0.5
                sensor_set['pointWidth'] = 20
                sensor_set['data_labels'] = {'enabled': False}
                set_data = []
                with open(filename) as f:
                    reader = csv.reader(f)
                    for line in reader:
                        start = dateutil.parser.parse(line[0])
                        start = dt_to_milliseconds(start)
                        if line[1] == '':
                            end = datetime.now()
                            end = dt_to_milliseconds(end)
                        else:
                            end = dateutil.parser.parse(line[1])
                            end = dt_to_milliseconds(end)
                        data = {'x':start, 'x2':end, 'y':index+1}
                        set_data.append(data)
                sensor_set['data'] = set_data
                sets.append(sensor_set)
            except Exception as e:
                pass
        return sets



    def get_thermostat_temperature_chart_data(self, api_key):

        data_slice = slice(-96, None)
        series = []

        api_log_filepath = f'{log_dir}/{api_key}-{self.identifier}'

        # Get log times (chartx-axis categories).
        try:
            categories = self.get_chart_categories(api_log_filepath, data_slice)
        except:
            categories = []
            pass

        # Get acutal temperatures (chart series).
        try:
            set_temperatures = self.get_actual_temperatures(api_log_filepath, data_slice)
            series_set_data = {"name": 'Actual Temperature', "data": set_temperatures}
            series.append(series_set_data)
        except:
            pass

        # Get set temperatures (chart series).
        try:
            set_temperatures = self.get_set_temperatures(api_log_filepath, data_slice)
            series_set_data = {"name": 'Set Temperature', "data": set_temperatures}
            series.append(series_set_data)
        except:
            pass

        # Get thermostat sensor temperatures (chart series).
        try:
            thermostat_temperatures = self.sensor.get_chart_temperatures(api_log_filepath, data_slice)
            series_thermostat_data = {"name": 'Thermostat', "data": thermostat_temperatures}
            series.append(series_thermostat_data)
        except:
            pass

        # Get thermostat remote sensor temperatures (chart series).
        for sensor in self.remote_sensors:
            try:
                sensor_temperatures = sensor.get_chart_temperatures(api_log_filepath, data_slice)
                series_sensor_temperatures = {"name": sensor.name, "data": sensor_temperatures}
                series.append(series_sensor_temperatures)
            except:
                pass

        chart_data = dict()
        chart_data['chart_id'] = 'temperature_chart'
        chart_data['chart'] = {"renderTo": 'temperature_chart', "type": 'spline', 'zoomType': 'x'}
        chart_data['title'] = {"text": 'Thermostat Temperatures'}
        chart_data['xAxis'] = {"title": {"text": 'Time'}, 'type':'datetime', "categories": categories, 'labels':{'format':'{value:%H:%M}'}}
        chart_data['yAxis'] = {"title": {"text": 'Temperature'}}
        chart_data['series'] = series

        return chart_data

    def get_chart_categories(self, api_log_filepath, data_slice):
        categories = []
        filename = f'{api_log_filepath}'
        with open(filename) as f:
            reader = csv.reader(f)
            for line in reader:
                dt = dateutil.parser.parse(line[0])
                ms = dt_to_milliseconds(dt)
                categories.append(ms)
        categories = categories[data_slice]
        return categories

    def get_actual_temperatures(self, api_log_filepath, data_slice):
        temperatures = []
        filename = f'{api_log_filepath}'
        with open(filename) as f:
            reader = csv.reader(f)
            for line in reader:
                temperatures.append(float(line[1]))
        temperatures = temperatures[data_slice]
        return temperatures

    def get_set_temperatures(self, api_log_filepath, data_slice):
        temperatures = []
        filename = f'{api_log_filepath}'
        with open(filename) as f:
            reader = csv.reader(f)
            for line in reader:
                temperatures.append(float(line[2]))
        temperatures = temperatures[data_slice]
        return temperatures


class RemoteSensor():
    def __init__(self, sensor):
        self.id = sensor['id']
        self.active = sensor['inUse']
        self.name = sensor['name']
        self.type = sensor['type']
        self.code = sensor['code']
        self.occupancy = True if sensor['capability'][1]['value'] == 'true' else False
        temperature = sensor['capability'][0]['value']
        if temperature != 'unknown':
            self.connected = True
            temperature = float(temperature)
            self.temperature = farenheit_to_degrees(temperature)
        else:
            self.connected = False
            self.temperature = None
        self.file_id = self.id[0:2] + self.id[-3:]

    def get_chart_temperatures(self, api_log_filepath, data_slice):
        temperatures = []
        filename = f'{api_log_filepath}-{self.file_id}'
        with open(filename) as f:
            reader = csv.reader(f)
            for line in reader:
                temperatures.append(float(line[1]))
        temperatures = temperatures[data_slice]
        return temperatures


class ThermostatSensor():
    def __init__(self, sensor):
        self.id = sensor['id']
        self.active = sensor['inUse']
        self.name = sensor['name']
        self.type = sensor['type']
        self.humidity = sensor['capability'][1]['value']
        self.occupancy = True if sensor['capability'][2]['value'] == 'true' else False
        self.active = True
        temperature = sensor['capability'][0]['value']
        if temperature != 'unknown':
            self.connected = True
            temperature = float(temperature)
            self.temperature = farenheit_to_degrees(temperature)
        else:
            self.connected = False
            self.temperature = None
        self.file_id = self.id[0:2] + self.id[-1:]

    def get_chart_temperatures(self, api_log_filepath, data_slice):
        temperatures = []
        filename = f'{api_log_filepath}-{self.file_id}'
        with open(filename) as f:
            reader = csv.reader(f)
            for line in reader:
                temperatures.append(float(line[1]))
        temperatures = temperatures[data_slice]
        return temperatures


class CurrentClimateData():
    def __init__(self, thermostat):
        if thermostat['events']:
            self.events = True
            holdClimateRef = thermostat['events'][0]['holdClimateRef']
            if holdClimateRef == "":
                self.mode = 'hold'
                temperature = thermostat['events'][0]['heatHoldTemp']
                self.temperature = farenheit_to_degrees(temperature)
            else:
                self.mode = holdClimateRef
                for climate in thermostat['program']['climates']:
                    if self.mode == climate['climateRef']:
                        temperature = climate['heatTemp']
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


class ClimateObj():
    def __init__(self, climate):
        self.ref = climate['climateRef']
        self.name = climate['name']
        temperature = climate['heatTemp']
        temperature = farenheit_to_degrees(temperature)
        self.temperature = temperature


def farenheit_to_degrees(temperature):
    temperature = (temperature - 320) * 5 / 90
    temperature = round(temperature, 2)
    return temperature


def degreees_to_farenheit(temperature):
    temperature = temperature * 90 / 5 + 320
    temperature = round(temperature, 2)
    return temperature
