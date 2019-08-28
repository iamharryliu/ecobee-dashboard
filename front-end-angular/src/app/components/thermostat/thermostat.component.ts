import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { AppService } from '../../app.service'

@Component({
  selector: 'app-thermostat',
  templateUrl: './thermostat.component.html',
  styleUrls: ['./thermostat.component.css']
})
export class ThermostatComponent implements OnInit {

  public thermostat: any;
  public thermostatSensor: any;
  public remoteSensors: any;
  public all_data_fetched = false;

  constructor(
    private _AppService: AppService,
    private _route: ActivatedRoute
  ) { }

  ngOnInit() {
    let key = (this._route.snapshot.paramMap.get('key'));
    let identifier = (this._route.snapshot.paramMap.get('identifier'));
    this.thermostat = { key: key, data: { identifier: identifier } }
    this.updateThermostat()
  }

  updateThermostat() {
    this._AppService.getThermostat(this.thermostat)
      .subscribe(data => {
        this.thermostat = data;
        this.remoteSensors = this.thermostat.data.remoteSensors;
        this.reserializeThermostatData();
        this.all_data_fetched = true;
      });
  }

  reserializeThermostatData() {
    this.reserializeSensors()
    this.reserializeActualTemperature()
    this.reserializeClimateData()
  }

  reserializeActualTemperature() {
    this.thermostat.actualTemperature = this.ecobeeTempToDegrees(this.thermostat.data.runtime.actualTemperature)
  }

  reserializeClimateData() {
    this.thermostat.currentClimateRef = this.currentClimateRef
    this.thermostat.currentClimateRefTemp = this.currentClimateRefTemp
  }

  get currentClimateRef() {
    var currentClimateRef: string;
    if (this.thermostat.data.events.length) {
      if (this.thermostat.data.events[0].holdClimateRef == '') {
        currentClimateRef = 'hold'
      }
      else {
        currentClimateRef = this.thermostat.data.events[0].holdClimateRef
      }
    }
    else {
      currentClimateRef = this.thermostat.data.program.currentClimateRef
    }
    return currentClimateRef
  }

  get currentClimateRefTemp() {
    var temperature: number
    if (this.thermostat.data.events.length) {
      temperature = this.thermostat.data.events[0].heatHoldTemp
    }
    else {
      for (let climate of this.thermostat.data.program.climates) {
        if (this.currentClimateRef == climate.climateRef) {
          temperature = climate.heatTemp
        }
      }
    }
    return this.ecobeeTempToDegrees(temperature)
  }

  reserializeSensors() {
    for (let i = 0; i < this.remoteSensors.length; i++) {
      let remoteSensor = this.remoteSensors[i]
      if (remoteSensor.type == 'ecobee3_remote_sensor') {
        remoteSensor.type = 'remote sensor'
      }
      let capabilities = remoteSensor.capability
      for (let j = 0; j < capabilities.length; j++) {
        let capability = capabilities[j]
        if (capability.type == 'temperature') {
          remoteSensor.temperature = this.ecobeeTempToDegrees(capability.value)
        }
        if (capability.type == 'humidity') {
          remoteSensor.humidity = capability.value
        }
        if (capability.type == 'occupancy') {
          remoteSensor.occupancy = capability.value == 'true'
        }
      }
    }
    this.remoteSensors.sort((b: string, a: string) => (a > b ? 1 : -1));
  }

  // Thermostat Actions

  setTemperature(temperature: string) {
    this._AppService.setTemperature(this.thermostat, parseFloat(temperature)).subscribe(response => {
      console.log(response);
      this.updateThermostat()
    });
  }

  setHvacMode(mode: string) {
    this.thermostat.hvacMode = mode
    this._AppService.setHvacMode(this.thermostat, mode).subscribe(response => {
      console.log(response);
      this.updateThermostat()
    })
  }

  setClimate(climate: string) {
    this._AppService.setClimate(this.thermostat, climate).subscribe(response => {
      console.log(response);
      this.updateThermostat();
    });
  }

  resume() {
    this._AppService.resume(this.thermostat).subscribe(response => {
      console.log(response);
      this.updateThermostat()
    });
  }

  // Utility

  ecobeeTempToDegrees(temperature: number) {
    temperature = (temperature / 10 - 32) * 5 / 9
    temperature = Math.round(temperature * 10) / 10
    return temperature
  }

}
