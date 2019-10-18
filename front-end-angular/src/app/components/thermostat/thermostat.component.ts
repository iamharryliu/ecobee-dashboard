import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { AppService } from '../../app.service'
import { App } from 'app';

@Component({
  selector: 'app-thermostat',
  templateUrl: './thermostat.component.html',
  styleUrls: ['./thermostat.component.css']
})
export class ThermostatComponent implements OnInit {

  public dataAvailable = false;
  public thermostat: any;
  public thermostatSensor: any;
  public remoteSensors: any;

  constructor(
    private _AppService: AppService,
    private _Route: ActivatedRoute
  ) { }

  ngOnInit() {
    let identifier = (this._Route.snapshot.paramMap.get('identifier'));
    this.loadData(identifier)
  }

  loadData(identifier: string = '') {
    this._AppService.getThermostat(identifier)
      .subscribe(data => {
        this.setData(data.thermostat)
        this.dataAvailable = true;
      });
  }

  updateThermostat() {
    this._AppService.getThermostat(this.thermostat.data.identifier)
      .subscribe(data => {
        this.setData(data.thermostat)
      });
  }

  setData(thermostat: App) {
    this.thermostat = thermostat;
    this.remoteSensors = thermostat.data.remoteSensors;
    this.reserializeSensors()
  }

  get currentClimateRefTemp() {
    return this._AppService.getCurrentClimateRefTemp(this.thermostat)
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

}
