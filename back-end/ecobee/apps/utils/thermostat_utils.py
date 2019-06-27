from ecobee.config import OCCUPANCY_HOURS
from ecobeeAPI.utils import farenheitX10_to_degrees
from ecobee.apps.utils.time_utils import get_X_hours_ago_dt, dt_to_milliseconds

import csv
from datetime import datetime
import dateutil.parser


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

        self.temp_log_dir = thermostat['temp_log_dir']
        self.occupancy_log_dir = thermostat['occupancy_log_dir']

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
        temperature = farenheitX10_to_degrees(temperature)
        return temperature

    def get_temperature(self, thermostat):
        temperature = thermostat['remoteSensors'][-1]['capability'][0]['value']
        temperature = float(temperature)
        temperature = farenheitX10_to_degrees(temperature)
        return temperature

    def get_occupancy_chart_data(self, api_key):

        categories = None
        series = None

        categories = self.get_occupancy_chart_categories()
        series = self.get_occupancy_chart_series(api_key)

        half_a_day_ago = get_X_hours_ago_dt(OCCUPANCY_HOURS)
        tickInterval = 1000 * 3600  # 1h in ms
        minorTickInterval = 1000 * 1800  # 30m in ms

        chart_data = dict()
        chart_data['chart_id'] = 'occupancy_chart'
        chart_data['chart'] = {"type": 'xrange', 'styledMode': True, 'zoomType': 'x'}
        chart_data['title'] = {"text": 'Occupancy Chart'}
        chart_data['xAxis'] = {'type': 'datetime', 'min': half_a_day_ago, 'tickInterval': tickInterval, 'minorTicks': True, 'minorTickInterval': minorTickInterval, 'dateTimeLabelFormats': {'hour': '%l:%M %P'}}
        chart_data['yAxis'] = {"title": {"text": ''}, 'categories': categories, 'reversed': True}
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
        series.append(self.get_thermostat_occupancy_set(api_key))
        sensor_sets = self.get_sensor_occupancy_sets(api_key)
        series += sensor_sets
        return series

    def get_thermostat_occupancy_set(self, api_key):
        filename = f'{self.occupancy_log_dir}/{api_key}-{self.identifier}-{self.sensor.file_id}'
        thermostat_set = dict()
        thermostat_set['name'] = 'Thermostat'
        # tehrmostart_set['pointPadding'] = 0
        thermostat_set['groupPadding'] = 0.5
        thermostat_set['pointWidth'] = 20
        thermostat_set['data_labels'] = {'enabled': False}
        set_data = []
        try:
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
                    data = {'x': start, 'x2': end, 'y': 0}
                    set_data.append(data)
        except:
            pass
        thermostat_set['data'] = set_data
        return thermostat_set

    def get_sensor_occupancy_sets(self, api_key):
        sets = []
        for index, sensor in enumerate(self.remote_sensors):
            filename = f'{self.occupancy_log_dir}/{api_key}-{self.identifier}-{sensor.file_id}'
            sensor_set = dict()
            sensor_set['name'] = sensor.name
            # tehrmostart_set['pointPadding'] = 0
            sensor_set['groupPadding'] = 0.5
            sensor_set['pointWidth'] = 20
            sensor_set['data_labels'] = {'enabled': False}
            set_data = []
            try:
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
                        data = {'x': start, 'x2': end, 'y': index + 1}
                        set_data.append(data)
            except:
                pass
            sensor_set['data'] = set_data
            sets.append(sensor_set)
        return sets

    def get_thermostat_temperature_chart_data(self, api_key):

        data_slice = slice(-96, None)
        series = []

        api_log_filepath = f'{self.temp_log_dir}/{api_key}-{self.identifier}'

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
        chart_data['xAxis'] = {"title": {"text": 'Time'}, 'type': 'datetime', "categories": categories, 'labels': {'format': '{value:%H:%M}'}}
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

    def getRemoteSensorData(self):
        sensors = []
        for sensor in self.remote_sensors:
            sensor = {
                'name': sensor.name,
                'active': sensor.active,
                'connected': sensor.connected,
                'type': sensor.type,
                'temperature': sensor.temperature,
                'occupancy': sensor.occupancy,
            }
            sensors.append(sensor)
        return sensors

    def getSensorData(self):
        sensor = {
            'name': self.sensor.name,
            'active': self.sensor.active,
            'connected': self.sensor.connected,
            'type': self.sensor.type,
            'temperature': self.sensor.temperature,
            'humidity': self.sensor.humidity,
            'occupancy': self.sensor.occupancy,
        }
        return sensor


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
            self.temperature = farenheitX10_to_degrees(temperature)
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
            self.temperature = farenheitX10_to_degrees(temperature)
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
                self.temperature = farenheitX10_to_degrees(temperature)
            else:
                self.mode = holdClimateRef
                for climate in thermostat['program']['climates']:
                    if self.mode == climate['climateRef']:
                        temperature = climate['heatTemp']
                        self.temperature = farenheitX10_to_degrees(temperature)
            self.end_date = thermostat['events'][0]['endDate']
            self.end_time = thermostat['events'][0]['endTime']
        else:
            self.events = False
            self.mode = thermostat['program']['currentClimateRef']
            for climate in thermostat['program']['climates']:
                if self.mode == climate['climateRef']:
                    temperature = climate['heatTemp']
                    self.temperature = farenheitX10_to_degrees(temperature)
            self.end_date = 'transition'
            self.end_time = 'transition'
        self.data = self.serializeData()

    def serializeData(self):
        data = {
            'mode': self.mode,
            'temperature': self.temperature,
            'events': self.events,
            'end_date': self.end_date,
            'end_time': self.end_time,

        }
        return data


class ClimateObj():
    def __init__(self, climate):
        self.ref = climate['climateRef']
        self.name = climate['name']
        temperature = climate['heatTemp']
        temperature = farenheitX10_to_degrees(temperature)
        self.temperature = temperature
