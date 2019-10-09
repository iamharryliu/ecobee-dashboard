import logging
import requests
import json
from datetime import datetime, timedelta
from ecobeeApp.utils import (
    degrees_to_farenheitX10,
    appDataParams,
    appDataParamsForThermostatsPage,
    runtimeColumns,
)

# URLs

ecobeeURL = "https://api.ecobee.com"
authorizeURL = f"{ecobeeURL}/authorize"
tokenURL = f"{ecobeeURL}/token"
thermostatURL = f"{ecobeeURL}/1/thermostat"
runtimeReportUrl = f"{ecobeeURL}/1/runtimeReport"

# Logging

from pathlib import Path

home_dir = str(Path.home())
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler(f"{home_dir}/logs/ecobeeApp.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class ecobeeApp:
    def __init__(
        self,
        api_key=None,
        authorization_code=None,
        access_token=None,
        refresh_token=None,
        config=None,
        name=None,
        logger=logger,
        db=None,
        dbType=None
    ):

        self.db = db
        self.dbType = dbType
        self.logger = logger

        if config:
            self.config = config
            self.name = config.name
            self.api_key = config.api_key
            self.authorization_code = config.authorization_code
            self.access_token = config.access_token
            self.refresh_token = config.refresh_token

        else:
            self.api_key = api_key
            self.authorization_code = authorization_code
            self.access_token = access_token
            self.refresh_token = refresh_token

    @staticmethod
    def test():
        params = {
            "response_type": "ecobeePin",
            "client_id": "test",
            "scope": "smartWrite",
        }
        try:
            requests.get(authorizeURL, params=params, timeout=1)
        except:
            return False
        else:
            return True

    @staticmethod
    def requestPinAndAuthorizationCode(api_key):
        params = {
            "response_type": "ecobeePin",
            "client_id": api_key,
            "scope": "smartWrite",
        }
        try:
            request = requests.get(authorizeURL, params=params)
        except:
            return None
        else:
            if request.status_code == requests.codes.ok:
                pin = request.json()["ecobeePin"]
                authorization_code = request.json()["code"]
                return pin, authorization_code
            else:
                return None

    @staticmethod
    def requestTokens(api_key, authorization_code):
        params = {
            "grant_type": "ecobeePin",
            "code": authorization_code,
            "client_id": api_key,
        }
        try:
            response = requests.post(tokenURL, params=params)
        except:
            return None
        else:
            if response.status_code == requests.codes.ok:
                access_token = response.json()["access_token"]
                refresh_token = response.json()["refresh_token"]
                return access_token, refresh_token
            else:
                return None

    def requestData(self):
        self.logger.info(f"{self.api_key}: Requesting data.")
        header = self.getRequestHeader()
        params = appDataParams
        try:
            response = requests.get(
                thermostatURL, headers=header, params=params, timeout=3
            )
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
        return response.json()

    def dataResponseNotOK(self):
        self.logResponseNotOK()
        if self.refreshTokens():
            return self.requestData()
        else:
            return None

    def getRequestHeader(self):
        header = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": "Bearer " + self.access_token,
        }
        return header

    def refreshTokens(self):
        self.logger.info(f"{self.api_key}: Requesting token refresh.")
        params = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.api_key,
        }
        response = requests.post(tokenURL, params=params)
        if response.status_code == requests.codes.ok:
            self.logResponseOK()
            self.updateTokens(response)
            return True
        else:
            self.logResponseNotOK()

    def updateTokens(self, response):
        """ Update app tokens. """
        self.logger.info(f"{self.api_key}: Requesting token update.")
        self.access_token = response.json()["access_token"]
        self.refresh_token = response.json()["refresh_token"]
        if self.db:
            self.writeTokensToDB()
        if self.dbType == 'Django':
            self.logger.info(f"{self.api_key}: Writing tokens to db.")
            self.config.access_token = self.access_token
            self.config.refresh_token = self.refresh_token
            self.config.save()


    def writeTokensToDB(self):
        """ Write tokens to db. """
        self.logger.info(f"{self.api_key}: Writing tokens to db.")
        self.config.access_token = self.access_token
        self.config.refresh_token = self.refresh_token
        self.db.session.commit()

    # Request Action

    def requestAction(self, body):
        self.logger.info(f"{self.api_key}: Requesting action.")
        header = self.getRequestHeader()
        params = {"format": "json"}
        try:
            response = requests.post(
                thermostatURL, headers=header, params=params, json=body
            )
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
            return self.requestAction(body)
        else:
            return False

    # Actions

    def resume(self, identifier, resume_all=False):
        logger.info(f"{self.api_key}-{identifier}: resume program")
        _type = "resumeProgram"
        params = {"resumeAll": resume_all}
        body = self.getRequestBody(identifier, params=params, _type=_type)
        return self.requestAction(body)

    def set_hvac_mode(self, identifier, hvac_mode):
        logger.info(f"{self.api_key}-{identifier}: set HVAC to {hvac_mode}")
        settings = {"hvacMode": hvac_mode}
        body = self.getRequestBody(identifier, settings=settings)
        return self.requestAction(body)

    def set_temperature_hold(
        self, identifier, temperature, hold_type="holdHours", holdHours=2
    ):
        logger.info(f"{self.api_key}-{identifier}: set temp to {temperature}")
        _type = "setHold"
        temperature = degrees_to_farenheitX10(temperature)
        params = {
            "holdType": hold_type,
            "coolHoldTemp": int(temperature),
            "heatHoldTemp": int(temperature),
            "holdHours": holdHours,
        }
        body = self.getRequestBody(identifier, params=params, _type=_type)
        return self.requestAction(body)

    def set_climate_hold(self, identifier, climate, hold_type="nextTransition"):
        logger.info(f"{self.api_key}-{identifier}: set climate to {climate}")
        _type = "setHold"
        params = {"holdType": hold_type, "holdClimateRef": climate}
        body = self.getRequestBody(identifier, params=params, _type=_type)
        return self.requestAction(body)

    def send_message(self, identifier, message="Hello world!"):
        logger.info(f"{self.api_key}-{identifier}: message - {message}")
        _type = "sendMessage"
        params = {"text": message[0:500]}
        body = self.getRequestBody(identifier, params=params, _type=_type)
        return self.requestAction(body)

    def create_vacation(self, identifier, vacation):
        logger.info(
            f"{self.api_key}-{identifier}: add vacation {vacation.name}/{vacation.temperature}C/{vacation.start_time} {vacation.end_time} to {vacation.end_date} {vacation.end_time})"
        )
        _type = "createVacation"
        params = {
            "name": vacation.name,
            "coolHoldTemp": vacation.temperature,
            "heatHoldTemp": vacation.temperature,
            "startDate": vacation.start_date,
            "startTime": vacation.start_time,
            "endDate": vacation.end_date,
            "endTime": vacation.end_time,
        }
        body = self.getRequestBody(identifier, params=params, _type=_type)
        return self.requestAction(body)

    # Action Request Body

    def getRequestBody(self, identifier, settings=None, params=None, _type=None):
        selection = self.getRequestSelection(identifier)
        body = dict()
        body["selection"] = selection
        if params:
            function = dict()
            function["type"] = _type
            function["params"] = params
            functions = [function]
            body["functions"] = functions
        if settings:
            body["thermostat"] = dict()
            body["thermostat"]["settings"] = settings
        return body

    def getRequestSelection(self, identifier):
        selection = {"selectionType": "thermostats", "selectionMatch": identifier}
        return selection

    # Log Messages

    def logRequestSuccessful(self):
        self.logger.debug(f"{self.api_key}: Request is successful.")

    def logRequestUnsuccessful(self):
        self.logger.debug(f"{self.api_key}: Request is unsuccessful.")

    def logResponseOK(self):
        self.logger.debug(f"{self.api_key}: Response is OK.")

    def logResponseNotOK(self):
        self.logger.warn(f"API-{self.api_key}: Response is not OK.")

    def getRuntimeReport(self, identifier):
        header = self.getRequestHeader()
        selection = self.getRequestSelection(identifier)
        now = datetime.utcnow()
        lastWeek = now - timedelta(days=7)
        lastWeek = lastWeek.strftime("%Y-%m-%d")
        startDate = lastWeek
        endDate = now.strftime("%Y-%m-%d")
        columns = runtimeColumns
        json = {
            "selection": selection,
            "startDate": startDate,
            "endDate": endDate,
            "startInverval": 0,
            "endInterval": 287,
            "columns": columns,
            "includeSensors": True,
        }

        params = {"json": str(json)}

        try:
            response = requests.get(runtimeReportUrl, headers=header, params=params)
        except:
            return None
        else:
            if response.status_code == requests.codes.ok:
                data = response.json()
                return data
            if self.refreshTokens():
                return self.getRuntimeReport(identifier)
            else:
                return None
