import { Component, OnInit } from '@angular/core';
import { APIService } from '../../api.service'

@Component({
  selector: 'app-thermostat',
  templateUrl: './thermostat.component.html',
  styleUrls: ['./thermostat.component.css']
})
export class ThermostatComponent implements OnInit {

  constructor(private _APIService: APIService) { }

  public thermostat;
  public all_data_fetched = false;
  ngOnInit() {
        this._APIService.getThermostat()
        .subscribe(data => {
            this.thermostat = data;
            this.all_data_fetched = true;

        });

  }

}
