import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../../user.service'


declare var $: any;

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  constructor(
    private _Router: Router,
    private _UserService: UserService
  ) { }

  ngOnInit() {
    $(document).ready(function () {
      $(document).click(function (event) {
        let clickover = $(event.target);
        let notNavbarToggler = !clickover.hasClass("navbar-toggler")
        let _opened = $(".collapse").is(":visible");
        // $(window).width() + 15 because of scrollbar width...
        if (_opened === true && notNavbarToggler && $(window).width() + 15 < 768) {
          $("button.navbar-toggler").click();
          console.log('click')
        }
      });
    });
  }

  get loginStatus() {
    return this._UserService.loginStatus
  }

  logoutUser() {
    this._UserService.logoutUser().subscribe(data => {
      if (data.success) {
        this._UserService.setLoginStatus(false)
        this._Router.navigate([''])
      }
      else {
        window.alert('Could not logout.')
      }
    })
  }

}
