import { Component, OnInit, Input } from '@angular/core';
import { APIService } from '../../../../api.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-message',
  templateUrl: './message.component.html',
  styleUrls: ['./message.component.css']
})
export class MessageComponent implements OnInit {

  @Input() public thermostat;
  public key;
  public identifier;
  public message = '';

  constructor(private _APIService: APIService,
    private _route: ActivatedRoute) { }

  ngOnInit() {
    this.key = (this._route.snapshot.paramMap.get('key'));
    this.identifier = (this._route.snapshot.paramMap.get('identifier'));
  }

  sendMessage() {
    this._APIService.sendMessage(this.key, this.identifier, this.message).subscribe(resp => {
      console.log(resp);
    })
  }

}
