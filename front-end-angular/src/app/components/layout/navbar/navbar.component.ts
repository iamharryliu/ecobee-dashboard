import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../../user.service'

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  constructor(
    private _Router: Router,
    private _UserService: UserService
  ) { }

  ngOnInit() { }

  get loginStatus() {
    return this._UserService.loginStatus
  }

  logoutUser() {
    this._UserService.logoutUser().subscribe(data => {
      if (data.success) {
        this._UserService.setLoginStatus(false)
        this._Router.navigate([''])
      }
      else {
        window.alert('Could not logout.')
      }
    })
  }

}
