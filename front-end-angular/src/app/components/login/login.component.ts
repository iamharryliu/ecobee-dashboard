import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms'
import { UserService } from '../../user.service'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private _FormBuilder: FormBuilder,
    private _Router: Router,
    private _UserService: UserService
  ) { }

  public loginForm = this._FormBuilder.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]],
    remember: [false, [Validators.required]]
  })

  ngOnInit() { }

  loginUser() {
    let data = this.loginForm.value
    this._UserService.loginUser(data).subscribe(data => {
      if (data.success) {
        this._UserService.setLoginStatus(true)
        this._Router.navigate(['apps'])
      } else {
        window.alert('Could not login.')
      }
    })
  }

  get email() {
    return this.loginForm.get('email')
  }

  get password() {
    return this.loginForm.get('password')
  }

}
