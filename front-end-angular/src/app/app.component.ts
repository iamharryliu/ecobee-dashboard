import { Component, OnInit } from '@angular/core';
import { UserService } from './user.service'
import { AppService } from './app.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {

  public dataLoaded = false;
  public apiRunning: boolean;

  constructor(
    private _UserService: UserService,
    private _AppService: AppService
  ) { }

  ngOnInit() {
    this._UserService.getLoginStatus().subscribe(data => {
      this._UserService.setLoginStatus(data.status);
      this._AppService.checkAPI().subscribe(data => {
        this.apiRunning = data.success
        this.dataLoaded = true;
      })
    })
  }

}