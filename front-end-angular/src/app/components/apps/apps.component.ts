import { Component, OnInit } from '@angular/core';
import { AppService } from '../../app.service'
import { Router } from '@angular/router';
import { UserService } from '../../user.service'

@Component({
  selector: 'app-apps',
  templateUrl: './apps.component.html',
  styleUrls: ['./apps.component.css']
})
export class AppsComponent implements OnInit {

  public apps = [];
  public authorizationCode: string;

  constructor(
    private _AppService: AppService,
    private _router: Router,
    private _UserService: UserService
  ) { }

  ngOnInit() {
    if (this._UserService.loginStatus) {
      this.fetchApps();
    }
  }

  fetchApps() {
    this._AppService.getApps()
      .subscribe(data => {
        this.apps = data;
      })
  }

  onSelect() {
    this._router.navigate(['/apps/thermostats'])
  }

  deleteApp(key: string) {
    this._AppService.deleteApp(key)
      .subscribe(r => {
        console.log(r)
        this.fetchApps()
      });
  }

  reAuthorizeApp(key: string) {
    this._AppService.authorizeApp(key).
      subscribe(response => {
        this.authorizationCode = response.data.authorization_code
        alert(response.data.pin)
      })
  }

  updateAppCredentials(key: string) {
    if (this.authorizationCode) {
      this._AppService.updateAppCredentials(key, this.authorizationCode).subscribe(response => {
        if (response.success) {
          alert('updated')
          this.fetchApps();
        }
        else {
          alert('Failed to reauthorize, try again.')
        }
      })

    }
    else {
      alert('Reauthorize App first.')
    }

  }
}
