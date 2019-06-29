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
  public key;
  public identifier;
  public all_data_fetched = false;

  constructor(private _APIService: APIService,
                private _route: ActivatedRoute) { }

  ngOnInit() {
        this.key = (this._route.snapshot.paramMap.get('key'));
        this.identifier = (this._route.snapshot.paramMap.get('identifier'));
        this._APIService.getThermostat(this.key, this.identifier)
        .subscribe(data => {
            this.thermostat = data;
            this.all_data_fetched = true;
        });

  }

}
