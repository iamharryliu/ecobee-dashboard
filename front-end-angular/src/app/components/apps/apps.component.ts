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

  public dataLoaded = false;
  public apps = [];
  public key: string;
  public pin: string;
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
        this.dataLoaded = true
      })
  }

  onSelect(key: string) {
    this._router.navigate([`/thermostats/${key}`])
  }

  deleteApp(key: string) {
    this._AppService.deleteApp(key)
      .subscribe(r => {
        console.log(r)
        this.fetchApps()
      });
  }

  reauthorizeApp(key: string) {
    this._AppService.authorizeApp(key).
      subscribe(response => {
        this.key = key
        this.pin = response.data.pin
        this.authorizationCode = response.data.authorization_code
      })
  }

  updateAppCredentials() {
    if (this.authorizationCode) {
      this._AppService.updateAppCredentials(this.key, this.authorizationCode).subscribe(response => {
        if (response.success) {
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
