import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../user.service'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(
    private _Router: Router,
    private _UserService: UserService) { }

  ngOnInit() {
  }

  loginUser(event) {

    const target = event.target
    const email = target.querySelector('#email').value
    const password = target.querySelector('#password').value
    const remember = target.querySelector('#rememberMe').checked

    let data = {
      'email': email,
      'password': password,
      'remember': remember
    }

    this._UserService.loginUser(data).subscribe(data => {
      if (data.success) {
        this._UserService.setLoginStatus(true)
        this._Router.navigate(['apps'])
      } else {
        window.alert('Could not login.')
      }
    })
  }
}
