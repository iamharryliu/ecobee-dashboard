import { Component, OnInit } from '@angular/core';
import { APIService } from '../../api.service'

@Component({
    selector: 'app-thermostats',
    templateUrl: './thermostats.component.html',
    styleUrls: ['./thermostats.component.css']
})
export class ThermostatsComponent implements OnInit {

    public thermostats = [];

    constructor(private _APIService: APIService) { }

    ngOnInit() {
        this._APIService.getThermostats()
        .subscribe(data => this.thermostats = data);
    }

}
