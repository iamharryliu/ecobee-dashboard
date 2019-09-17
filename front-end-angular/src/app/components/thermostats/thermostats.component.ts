import { Component, OnInit } from '@angular/core';
import { AppService } from '../../app.service';
import { ActivatedRoute, Router } from '@angular/router';

import { Thermostat } from '../../../../app'

@Component({
  selector: 'app-thermostats',
  templateUrl: './thermostats.component.html',
  styleUrls: ['./thermostats.component.css']
})

export class ThermostatsComponent implements OnInit {

  public all_data_fetched = false;
  public thermostats = [];
  public key: string;

  constructor(
    private _Route: ActivatedRoute,
    private _AppService: AppService,
    private _Router: Router,
  ) { }

  ngOnInit() {
    let key = this._Route.snapshot.paramMap.get('key')
    if (key) {
      this._AppService.getAppThermostats(key)
        .subscribe(data => {
          this.thermostats = data;
          this.all_data_fetched = true;
        });
    }
    else {

      this._AppService.getUserThermostats()
        .subscribe(data => {
          this.thermostats = data;
          this.all_data_fetched = true;
        });
    }
  }

  view(thermostat: Thermostat) {
    let key = thermostat.api_key;
    let identifier = thermostat.data.identifier;
    this._Router.navigate(['/thermostats/', key, identifier])
  }

}
