import { Component, OnInit } from '@angular/core';
import { APIService } from '../../api.service'
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-thermostat',
  templateUrl: './thermostat.component.html',
  styleUrls: ['./thermostat.component.css']
})
export class ThermostatComponent implements OnInit {

  public thermostat;
  public all_data_fetched = false;

  constructor(private _APIService: APIService,
    private _route: ActivatedRoute) { }

  ngOnInit() {
    let key = (this._route.snapshot.paramMap.get('key'));
    let identifier = (this._route.snapshot.paramMap.get('identifier'));
    this.thermostat = { key: key, identifier: identifier }
    this._APIService.getThermostat(this.thermostat)
      .subscribe(data => {
        this.thermostat = data;
        this.all_data_fetched = true;
      });

  }

  updateThermostat() {
    this._APIService.getThermostat(this.thermostat)
      .subscribe(data => {
        this.thermostat = data;
      });
  }

}
