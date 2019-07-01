import { Component, OnInit } from '@angular/core';
import { APIService } from '../../api.service'
import { Router } from '@angular/router';

@Component({
  selector: 'app-apps',
  templateUrl: './apps.component.html',
  styleUrls: ['./apps.component.css']
})
export class AppsComponent implements OnInit {

  public apis = [];

  constructor(private _APIService: APIService,
              private _router: Router) { }

  ngOnInit() {
    this._APIService.getAPIS()
    .subscribe(data => {this.apis = data; console.log(data)})
  }

  onSelect(key){
    this._router.navigate(['/apps', key])
  }

  deleteAPI(key){
    this._APIService.deleteAPI(key)
  }

}
