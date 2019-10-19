import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { AppService } from '../../app.service'
import { RemoteSensor } from 'app';

@Component({
  selector: 'app-thermostat',
  templateUrl: './thermostat.component.html',
  styleUrls: ['./thermostat.component.css']
})
export class ThermostatComponent implements OnInit {

  public dataAvailable = false;
  public thermostat: any;
  public thermostatSensor: any;
  public sensors: any;

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
        this.thermostat = data.thermostat;
        this.dataAvailable = true;
      });
  }

  updateThermostat() {
    this._AppService.getThermostat(this.thermostat.data.identifier)
      .subscribe(data => {
        this.thermostat = data.thermostat;
      });
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

  get currentClimateRefTemp() {
    return this._AppService.getCurrentClimateRefTemp(this.thermostat)
  }

}
