import { Injectable } from '@angular/core';
import { App, RemoteSensor } from 'app';

@Injectable({
  providedIn: 'root'
})
export class ThermostatService {

  constructor() { }

  public temperatureOptions = [18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0];

  ecobeeTempToDegrees(temperature: number) {
    let temperatureAsFarenheit = temperature / 10
    let temperatureAsDegrees = this.farenheitToDegrees(temperatureAsFarenheit)
    temperatureAsDegrees = Math.round(temperatureAsDegrees * 10) / 10
    return temperatureAsDegrees
  }

  farenheitToDegrees = (temperature: number) => (temperature - 32) * 5 / 9

  getCurrentClimateRef(thermostat: App) {
    return thermostat.data.events.length ? this.getEventClimateRef(thermostat) : thermostat.data.program.currentClimateRef
  }

  getEventClimateRef(thermostat: App) {
    return thermostat.data.events[0].holdClimateRef == '' ? 'hold' : thermostat.data.events[0].holdClimateRef
  }

  getCurrentClimateRefTemp(thermostat: App) {
    let temperature = thermostat.data.events.length ? thermostat.data.events[0].heatHoldTemp : this.getClimateRefTemp(thermostat)
    return this.ecobeeTempToDegrees(temperature)
  }

  getClimateRefTemp(thermostat: App) {
    for (let climate of thermostat.data.program.climates) {
      if (this.getCurrentClimateRef(thermostat) == climate.climateRef) return climate.heatTemp
    }
  }

  sortSensors = (a: RemoteSensor, b: RemoteSensor) => a.id.localeCompare(b.id);

}
