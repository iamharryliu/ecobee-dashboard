import { Component, OnInit } from '@angular/core';
import { APIService } from '../../api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-thermostats',
  templateUrl: './thermostats.component.html',
  styleUrls: ['./thermostats.component.css']
})
export class ThermostatsComponent implements OnInit {

  public thermostats = [];
  public all_data_fetched = false;
  public key: string;

  constructor(private _APIService: APIService,
    private _Router: Router, ) { }

  ngOnInit() {
    this._APIService.getUserThermostats()
      .subscribe(data => {
        this.thermostats = data;
        this.all_data_fetched = true;
      });
  }

  view(thermostat) {
    let key = thermostat.key;
    let identifier = thermostat.identifier;
    this._Router.navigate(['/apis', key, identifier])
  }

}
