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
  public dataAvailable = false;

  constructor(
    private _AppService: AppService,
    private _Route: ActivatedRoute
  ) { }

  ngOnInit() {
    let key = (this._Route.snapshot.paramMap.get('key'));
    let identifier = (this._Route.snapshot.paramMap.get('identifier'));
    this.thermostat = { key: key, data: { identifier: identifier } }
    this.getThermostatData(identifier)
  }

  getThermostatData(identifier: string) {
    this._AppService.getThermostat(identifier)
      .subscribe(data => {
        this.thermostat = data.thermostat;
        this.remoteSensors = this.thermostat.data.remoteSensors;
        this.reserializeThermostatData();
        this.dataAvailable = true;
      });
  }

  updateThermostat() {
    this._AppService.getThermostat(this.thermostat.data.identifier)
      .subscribe(data => {
        this.thermostat = data.thermostat;
        this.remoteSensors = this.thermostat.data.remoteSensors;
        this.reserializeThermostatData();
      });
  }

  reserializeThermostatData() {
    this.reserializeSensors()
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
          remoteSensor.temperature = this._AppService.ecobeeTempToDegrees(capability.value)
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
      console.log('Successfully set temperature.');
      this.updateThermostat()
    });
  }

  setHvacMode(mode: string) {
    this.thermostat.hvacMode = mode
    this._AppService.setHvacMode(this.thermostat, mode).subscribe(response => {
      console.log('Successfully set HVAC mode.');
      this.updateThermostat()
    })
  }

  setClimate(climate: string) {
    this._AppService.setClimate(this.thermostat, climate).subscribe(response => {
      console.log('Successfully set climate.');
      this.updateThermostat();
    });
  }

  resume() {
    this._AppService.resume(this.thermostat).subscribe(response => {
      console.log('Successfully resumed thermostat program.');
      this.updateThermostat()
    });
  }

}
