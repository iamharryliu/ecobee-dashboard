import { Component, OnInit } from '@angular/core';
import { APIService } from '../../api.service';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';

@Component({
    selector: 'app-thermostats',
    templateUrl: './thermostats.component.html',
    styleUrls: ['./thermostats.component.css']
})
export class ThermostatsComponent implements OnInit {

    public thermostats = [];
    public all_data_fetched = false;
    public key

    constructor(private _APIService: APIService,
                private _router: Router,
                private _route: ActivatedRoute) { }

    ngOnInit() {
        this.key = (this._route.snapshot.paramMap.get('key'));
        this._APIService.getThermostats(this.key)
        .subscribe(data => {
            this.thermostats = data;
            this.all_data_fetched = true;
        });
    }

  view(key, identifier){
    this._router.navigate(['/apps', key, identifier])
  }

}
