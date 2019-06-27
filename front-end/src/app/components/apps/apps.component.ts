import { Component, OnInit } from '@angular/core';
import { APIService } from '../../api.service'

@Component({
  selector: 'app-apps',
  templateUrl: './apps.component.html',
  styleUrls: ['./apps.component.css']
})
export class AppsComponent implements OnInit {

  public apis = [];

  constructor(private _APIService: APIService) { }

  ngOnInit() {
    this._APIService.getAPIS()
    .subscribe(data => this.apis = data);
  }

  deleteAPI(name){
    console.log('delete')
  }

}
