import { Component, OnInit, Input } from '@angular/core';
import { APIService } from '../../../../api.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-message',
  templateUrl: './message.component.html',
  styleUrls: ['./message.component.css']
})
export class MessageComponent implements OnInit {

  @Input() public thermostat: any;
  public message = '';

  constructor(private _APIService: APIService) { }

  ngOnInit() { }

  sendMessage() {
    this._APIService.sendMessage(this.thermostat, this.message).subscribe(resp => {
      console.log(resp);
      this.message = '';
    })
  }

}
