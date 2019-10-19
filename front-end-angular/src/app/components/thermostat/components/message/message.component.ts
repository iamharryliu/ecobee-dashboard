import { Component, OnInit, Input } from '@angular/core';
import { AppService } from '../../../../app.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-message',
  templateUrl: './message.component.html',
  styleUrls: ['./message.component.css']
})
export class MessageComponent implements OnInit {

  @Input() public thermostat: any;
  public message = '';

  constructor(private _AppService: AppService) { }

  ngOnInit() { }

  sendMessage() {
    this._AppService.sendMessage(this.thermostat, this.message).subscribe(_ => {
      console.log('Successfully sent message.');
      this.message = '';
    })
  }

}
