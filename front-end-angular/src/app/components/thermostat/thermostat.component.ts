import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AppService } from '../../app.service'
import { ThermostatService } from 'src/app/thermostat.service';

@Component({
  selector: 'app-thermostat',
  templateUrl: './thermostat.component.html',
  styleUrls: ['./thermostat.component.css']
})
export class ThermostatComponent implements OnInit {

  public dataAvailable = false;
  public thermostat: any;

  constructor(
    private _AppService: AppService,
    private _ThermostatService: ThermostatService,
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

  get currentClimateRefTemp() {
    return this._ThermostatService.getCurrentClimateRefTemp(this.thermostat)
  }

  get sensors() {
    return this.thermostat.data.remoteSensors.sort(this._ThermostatService.sortSensors)
  }

}
