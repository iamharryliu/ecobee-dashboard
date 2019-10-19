import { Injectable } from '@angular/core';
import { App, RemoteSensor } from 'app';

@Injectable({
  providedIn: 'root'
})
export class ThermostatService {

  constructor() { }

  ecobeeTempToDegrees(temperature: number) {
    temperature = (temperature / 10 - 32) * 5 / 9
    temperature = Math.round(temperature * 10) / 10
    return temperature
  }

  getCurrentClimateRef(thermostat: App) {
    let currentClimateRef: string;
    if (thermostat.data.events.length) {
      if (thermostat.data.events[0].holdClimateRef == '') {
        currentClimateRef = 'hold'
      }
      else {
        currentClimateRef = thermostat.data.events[0].holdClimateRef
      }
    }
    else {
      currentClimateRef = thermostat.data.program.currentClimateRef
    }
    return currentClimateRef
  }

  getCurrentClimateRefTemp(thermostat: App) {
    let temperature: number
    if (thermostat.data.events.length) {
      temperature = thermostat.data.events[0].heatHoldTemp
    }
    else {
      for (let climate of thermostat.data.program.climates) {
        if (this.getCurrentClimateRef(thermostat) == climate.climateRef) {
          temperature = climate.heatTemp
        }
      }
    }
    return this.ecobeeTempToDegrees(temperature)
  }

  sortSensors(a: RemoteSensor, b: RemoteSensor) {
    if (a.id < b.id) {
      return -1;
    }
    if (a.id > b.id) {
      return 1;
    }
    return 0;
  }

}
