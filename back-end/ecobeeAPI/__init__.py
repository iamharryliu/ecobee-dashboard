import logging
import requests
import json
from ecobeeAPI.utils import degrees_to_farenheitX10

ECOBEE_URL = 'https://api.ecobee.com'
logger = logging.getLogger(__name__)


class EcobeeAPI():
    def __init__(self, api_key=None, authorization_code=None, access_token=None, refresh_token=None, config=None, name=None, logger=logger, db=None):

        if config:
            self.config = config
            self.db = db
            self.logger = logger
            self.name = config.name
            self.api_key = config.api_key
            self.authorization_code = config.authorization_code
            self.access_token = config.access_token
            self.refresh_token = config.refresh_token
            self.data = self.requestData()

        else:
            self.logger = logger
            self.name = name
            self.api_key = api_key
            self.authorization_code = authorization_code
            self.access_token = access_token
            self.refresh_token = refresh_token
            self.data = self.requestData()

    @staticmethod
    def requestPinAndAuthorizationCode(api_key):
        url = f'{ECOBEE_URL}/authorize'
        params = {
            'response_type': 'ecobeePin',
            'client_id': api_key,
            'scope': 'smartWrite'
        }
        try:
            request = requests.get(url, params=params)
        except:
            return None
        else:
            if request.status_code == requests.codes.ok:
                pin = request.json()['ecobeePin']
                authorization_code = request.json()['code']
                return pin, authorization_code
            else:
                return None

    @staticmethod
    def requestTokens(api_key, authorization_code):
        url = f'{ECOBEE_URL}/token'
        params = {'grant_type': 'ecobeePin',
                  'code': authorization_code,
                  'client_id': api_key}
        try:
            response = requests.post(url, params=params)
        except:
            return None
        else:
            if response.status_code == requests.codes.ok:
                access_token = response.json()['access_token']
                refresh_token = response.json()['refresh_token']
                return access_token, refresh_token
            else:
                return None

    def requestData(self):
        self.logger.info(f'API-{self.api_key}: Requesting JSON data.')
        url = f'{ECOBEE_URL}/1/thermostat'
        header = self.getRequestHeader()
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
        except Exception as e:
            print(e)
            self.logRequestUnsuccessful()
            return None
        else:
            self.logRequestSuccessful()
            return self.handleDataResponse(response)

    def handleDataResponse(self, response):
        if response.status_code == requests.codes.ok:
            return self.dataResponseOK(response)
        else:
            return self.dataResponseNotOK()

    def dataResponseOK(self, response):
        self.logResponseOK()
        return json.loads(response.text)

    def dataResponseNotOK(self):
        self.logResponseNotOK()
        if self.refreshTokens():
            return self.requestData()
        else:
            return None

    def getRequestHeader(self):
        header = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': 'Bearer ' + self.access_token
        }
        return header

    def refreshTokens(self):
        self.logger.info(f'API-{self.api_key}: Requesting token refresh.')
        url = f'{ECOBEE_URL}/token'
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.api_key
        }
        response = requests.post(url, params=params)
        if response.status_code == requests.codes.ok:
            self.logResponseOK()
            self.updateTokens(response)
            return True
        else:
            self.logResponseNotOK()

    def updateTokens(self, response):
        self.access_token = response.json()['access_token']
        self.refresh_token = response.json()['refresh_token']
        if self.db:
            self.writeTokensToDB()

    def writeTokensToDB(self):
        self.logger.info(f'API-{self.api_key}: Writing tokens to db')
        self.config.access_token = self.access_token
        self.config.refresh_token = self.refresh_token
        self.db.session.commit()

    # Request Action

    def requestAction(self, body, log_msg_action):
        self.logger.info(f'API-{self.api_key}: Requesting action.')
        url = f'{ECOBEE_URL}/1/thermostat'
        header = self.getRequestHeader()
        params = {
            'format': 'json'
        }
        try:
            response = requests.post(url, headers=header, params=params, json=body)
        except Exception as e:
            print(e)
            self.logRequestUnsuccessful()
            return False
        else:
            self.logRequestSuccessful()
            return self.handleActionResponse(response)

    def handleActionResponse(self, response):
        if response.status_code == requests.codes.ok:
            return self.actionResponseOK()
        else:
            return self.actionResponseNotOK()

    def actionResponseOK(self):
        self.logResponseOK()
        return True

    def actionResponseNotOK(self):
        self.logResponseNotOK()
        if self.refreshTokens():
            return self.requestAction(body, log_msg_action)
        else:
            return False

    # Actions

    def resume(self, identifier, resume_all=False):
        print('Resume.')
        _type = "resumeProgram"
        params = {"resumeAll": resume_all}
        body = self.getRequestBody(identifier, params=params, _type=_type)
        log_msg_action = f'Thermostat: {identifier} program resumed'
        return self.requestAction(body, log_msg_action)

    def set_hvac_mode(self, identifier, hvac_mode):
        print(f'HVAC mode set to {hvac_mode}')
        settings = {"hvacMode": hvac_mode}
        body = self.getRequestBody(identifier, settings=settings)
        log_msg_action = f'Thermostat: {identifier} HVAC mode set to {hvac_mode}'
        return self.requestAction(body, log_msg_action)

    def set_temperature_hold(self, identifier, temperature, hold_type="holdHours", holdHours=2):
        print(f'Temperature set to {temperature}')
        _type = "setHold"
        temperature = degrees_to_farenheitX10(temperature)
        params = {
            "holdType": hold_type,
            "coolHoldTemp": int(temperature),
            "heatHoldTemp": int(temperature),
            "holdHours": holdHours
        }
        body = self.getRequestBody(identifier, params=params, _type=_type)
        log_msg_action = f"Themrostat: {identifier} set to hold {temperature}"
        return self.requestAction(body, log_msg_action)

    def set_climate_hold(self, identifier, climate, hold_type="nextTransition"):
        print(f'Climate set to {climate}')
        _type = "setHold"
        params = {"holdType": hold_type, "holdClimateRef": climate}
        body = self.getRequestBody(identifier, params=params, _type=_type)
        log_msg_action = f"Thermostat: {identifier} set to hold {climate} climate"
        return self.requestAction(body, log_msg_action)

    def send_message(self, identifier, message="Hello world!"):
        print(f'Message sent.')
        _type = "sendMessage"
        params = {"text": message[0:500]}
        body = self.getRequestBody(identifier, params=params, _type=_type)
        log_msg_action = f"Send Message: {message}"
        return self.requestAction(body, log_msg_action)

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
        body = self.getRequestBody(identifier, params=params, type=_type)
        log_msg_action = f"Thermostat: {idenfifier} add vacation ({name} / {vacation.temperature} / {vacation.start_time} {vacation.end_time} to {vacation.end_date} {vacation.end_time})"
        return self.requestAction(body, log_msg_action)

    # Action Request Body

    def getRequestBody(self, identifier, settings=None, params=None, _type=None):
        selection = self.requestBodySelection(identifier)
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

    def requestBodySelection(self, identifier):
        selection = {
            "selectionType": "thermostats",
            "selectionMatch": identifier
        }
        return selection

    # Log Messages

    def logRequestSuccessful(self):
        self.logger.info(f'API-{self.api_key}: Request is successful.')

    def logRequestUnsuccessful(self):
        self.logger.warn(f'API-{self.api_key}: Request is unsuccessful.')

    def logResponseOK(self):
        self.logger.info(f'API-{self.api_key}: Response is OK.')

    def logResponseNotOK(self):
        self.logger.warn(f'API-{self.api_key}: Response is not OK.')

    # Str

    def __str__(self):
        return json.dumps(self.data, indent=2)
