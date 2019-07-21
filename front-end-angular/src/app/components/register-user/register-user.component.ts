import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../user.service'

@Component({
  selector: 'app-register-user',
  templateUrl: './register-user.component.html',
  styleUrls: ['./register-user.component.css']
})
export class RegisterUserComponent implements OnInit {

  constructor(
    private _Router: Router, private _UserService: UserService) { }

  ngOnInit() {
  }

  registerUser(event) {
    const target = event.target
    const username = target.querySelector('#username').value
    const email = target.querySelector('#email').value
    const password = target.querySelector('#password').value
    let data = {
      'username': username,
      'email': email,
      'password': password,
    }
    this._UserService.registerUser(data).subscribe(data => {
      if (data.success) {
        this._Router.navigate(['login'])
      } else {
        window.alert('Could not register.')
      }
    })
  }

}
