import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms'
import { AppService } from 'src/app/app.service'
import { Router } from '@angular/router';

declare var $: any;

@Component({
  selector: 'app-register-app',
  templateUrl: './register-app.component.html',
  styleUrls: ['./register-app.component.css']
})
export class RegisterAppComponent implements OnInit {

  constructor(
    private _FormBuilder: FormBuilder,
    private _AppService: AppService,
    private _router: Router
  ) { }

  public nameMinLength = 4;
  public keyLength = 32;
  public authorizationCodeLength = 32;

  public authorizeForm = this._FormBuilder.group({
    key: ['', [Validators.required, Validators.minLength(this.keyLength), Validators.maxLength(this.keyLength)]]
  })
  public pin: string;
  public registerForm = this._FormBuilder.group({
    key: [''],
    name: ['', [Validators.required, Validators.minLength(this.nameMinLength)]],
    authorizationCode: [''],
  })

  ngOnInit() { }

  authorizeApp() {
    this._AppService.authorizeApp(this.authorizeForm.value.key)
      .subscribe(response => {
        if (response.success) {
          console.log('Successfully authorized app.')
          this.pin = response.data.pin
          this.registerForm.patchValue({ key: this.authorizeForm.value.key, authorizationCode: response.data.authorization_code })
          $('#exampleModal').modal('toggle')
        }
        else {
          console.log('Could not successfully authorize app.')
        }
      });
  }

  registerApp() {
    this._AppService.createApp(this.registerForm.value)
      .subscribe(response => {
        if (response.success) {
          console.log('Successfully registered app.')
          $('#exampleModal').modal('toggle')
          this._router.navigate(['/apps'])
        }
        else {
          alert('Could not register app.')
        }
      });
  }

  get key() {
    return this.authorizeForm.get('key')
  }

  get name() {
    return this.registerForm.get('name')
  }


}
