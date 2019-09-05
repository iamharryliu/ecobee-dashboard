import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../user.service';
import { FormBuilder, Validators } from '@angular/forms'

import { AbstractControl } from '@angular/forms';
function PasswordValidator(control: AbstractControl): { [key: string]: boolean } | null {
  const password = control.get('password')
  const confirmPassword = control.get('confirmPassword')
  return password && confirmPassword && password.value != confirmPassword.value ?
    { 'misMatch': true } :
    null;
}

@Component({
  selector: 'app-register-user',
  templateUrl: './register-user.component.html',
  styleUrls: ['./register-user.component.css']
})
export class RegisterUserComponent implements OnInit {

  public usernameMinLength = 8;
  public passwordMinLength = 8;

  constructor(
    private _FormBuilder: FormBuilder,
    private _Router: Router,
    private _UserService: UserService
  ) { }

  public registerForm = this._FormBuilder.group({
    username: ['', [Validators.required, Validators.minLength(this.usernameMinLength)]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(this.passwordMinLength)]],
    confirmPassword: ['', [Validators.required]]
  }, { validator: PasswordValidator })

  ngOnInit() { }

  registerUser() {
    let data = {
      username: this.registerForm.value.username,
      email: this.registerForm.value.email,
      password: this.registerForm.value.password
    }
    this._UserService.registerUser(data).subscribe(data => {
      if (data.success) {
        this._Router.navigate(['login'])
      } else {
        window.alert('Could not register.')
      }
    })
  }

  get username() {
    return this.registerForm.get('username')
  }

  get email() {
    return this.registerForm.get('email')
  }

  get password() {
    return this.registerForm.get('password')
  }

  get confirmPassword() {
    return this.registerForm.get('confirmPassword')
  }

}
