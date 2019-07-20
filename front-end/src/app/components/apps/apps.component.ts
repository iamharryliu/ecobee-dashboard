import { Component, OnInit } from '@angular/core';
import { APIService } from '../../api.service'
import { Router } from '@angular/router';
import { UserService } from '../../user.service'

@Component({
  selector: 'app-apps',
  templateUrl: './apps.component.html',
  styleUrls: ['./apps.component.css']
})
export class AppsComponent implements OnInit {

  public apps = [];

  constructor(
    private _APIService: APIService,
    private _router: Router,
    private _UserService: UserService
  ) { }

  ngOnInit() {
    if (this._UserService.loginStatus) {
      this.fetchApps()
    }
  }

  fetchApps() {
    this._APIService.getApps()
      .subscribe(data => {
        this.apps = data;
      })
  }

  onSelect(key: string) {
    this._router.navigate(['/apis', key])
  }

  deleteApp(key: string) {
    this._APIService.deleteApp(key)
      .subscribe(r => {
        console.log(r)
        this.fetchApps()
      });
  }

}
