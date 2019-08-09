import { Component, OnInit } from '@angular/core';
import { AppService } from '../../app.service';
import { Router } from '@angular/router';

import { Thermostat } from '../../../../app'

@Component({
  selector: 'app-thermostats',
  templateUrl: './thermostats.component.html',
  styleUrls: ['./thermostats.component.css']
})
export class ThermostatsComponent implements OnInit {

  public thermostats = [];
  public all_data_fetched = false;
  public key: string;

  constructor(private _AppService: AppService,
    private _Router: Router, ) { }

  ngOnInit() {
    this._AppService.getUserThermostats()
      .subscribe(data => {
        this.thermostats = data;
        this.all_data_fetched = true;
      });
  }

  view(thermostat: Thermostat) {
    let key = thermostat.api_key;
    let identifier = thermostat.data.identifier;
    this._Router.navigate(['/apps/thermostats/', key, identifier])
  }

}
