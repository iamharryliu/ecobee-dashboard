import { Component, OnInit } from '@angular/core';
import { APIService } from '../../api.service'
import { Router } from '@angular/router';

class appForm {
  constructor(
    public appName: string,
    public apiKey: string,
    public authorizationCode: string
  ) { }
}

@Component({
  selector: 'app-register-api',
  templateUrl: './register-api.component.html',
  styleUrls: ['./register-api.component.css']
})
export class RegisterApiComponent implements OnInit {

  constructor(private _APIService: APIService,
    private _router: Router) { }

  form = new appForm('', '', '')

  ngOnInit() { }

  authorizeApp() {
    // console.log(this.form.apiKey)
    this._APIService.authorizeApp(this.form.apiKey)
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
    this._APIService.createApp(this.form)
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
