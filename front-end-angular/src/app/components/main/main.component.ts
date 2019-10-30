import { Component, OnInit } from '@angular/core';
import { UserService } from 'src/app/user.service'

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  constructor(
    private _UserService: UserService
  ) { }

  ngOnInit() { }

  get loginStatus() {
    return this._UserService.loginStatus
  }

}
