def degrees_to_farenheitX10(temperature):
    temperature = degrees_to_farenheit(temperature) * 10
    return temperature


def farenheitX10_to_degrees(temperature):
    temperature = farenheit_to_degrees(temperature / 10)
    temperature = round(temperature, 2)
    return temperature


def degrees_to_farenheit(temperature):
    return temperature * 9 / 5 + 32


def farenheit_to_degrees(temperature):
    return (temperature - 32) * 5 / 9


format = "json"


bodyForThermostatsPage = {"selection": {"selectionType": "registered"}}

appDataParamsForThermostatsPage = {format: str(bodyForThermostatsPage)}

bodyForThermostatPage = {
    "selection": {
        "selectionType": "registered",
        "includeRuntime": "true",
        "includeSensors": "true",
        "includeProgram": "true",
        "includeEvents": "true",
        "includeAlerts": "true",
        "includeSettings": "true",
    }
}

appDataParams = {format: str(bodyForThermostatPage)}


runtimeColumns = "hvacMode,outdoorHumidity,outdoorTemp,zoneCalendarEvent,zoneCoolTemp,zoneHeatTemp,zoneOccupancy,zoneHumidity,zoneAveTemp"
