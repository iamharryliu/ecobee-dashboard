import { Component, OnInit } from '@angular/core';
import { AppService } from '../../app.service'
import { Router } from '@angular/router';

class appForm {
  constructor(
    public appName: string,
    public apiKey: string,
    public authorizationCode: string
  ) { }
}

@Component({
  selector: 'app-register-app',
  templateUrl: './register-app.component.html',
  styleUrls: ['./register-app.component.css']
})
export class RegisterAppComponent implements OnInit {

  constructor(private _AppService: AppService,
    private _router: Router) { }

  form = new appForm('', '', '')

  ngOnInit() { }

  authorizeApp() {
    this._AppService.authorizeApp(this.form.apiKey)
      .subscribe(r => {
        this.handleAuthorizeAppResponse(r)
      });
  }

  handleAuthorizeAppResponse(r: any) {
    if (r.success) {
      console.log('Successfully authorized app.')
      alert(r.data.pin)
      this.form.authorizationCode = r.data.authorization_code
    }
    else {
      console.log('Could not successfully authorize app.')
    }
  }

  onApiKeyChange() {
    this.form.authorizationCode = ''
  }

  onSubmit() {
    this._AppService.createApp(this.form)
      .subscribe(r => {
        if (r.success) {
          this._router.navigate(['/apps'])
        }
        else {
          alert('Could not register app.')
        }
      });
  }


}
