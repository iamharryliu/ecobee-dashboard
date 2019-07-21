import { Component, OnInit } from '@angular/core';
import { UserService } from './user.service'
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  constructor(
    private _UserService: UserService
  ) { }

  ngOnInit() {
    this._UserService.getLoginStatus().subscribe(data => {
      this._UserService.setLoginStatus(data.success)
    })
  }
}