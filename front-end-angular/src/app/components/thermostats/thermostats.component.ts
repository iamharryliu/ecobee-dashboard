import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AppService } from '../../app.service';
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
    private _AppService: AppService
  ) { }

  ngOnInit() {
    let key = this._Route.snapshot.paramMap.get('key')
    if (key) {
      this.key = key
      this.getAppThermostats(key)
    }
    else {
      this.key = ''
      this.getUserThermostats()
    }
  }

  getAppThermostats(key: string) {
    this._AppService.getAppThermostats(key)
      .subscribe(data => {
        this.setData(data)
      });
  }

  getUserThermostats() {
    this._AppService.getUserThermostats()
      .subscribe(data => {
        this.setData(data)
      });
  }

  setData(data: Thermostat[]) {
    this.thermostats = data;
    this.all_data_fetched = true;
  }

}
