import { Component, OnInit, Input } from '@angular/core';
import { APIService } from '../../../../api.service'
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {

  @Input() public thermostat;

  public key;
  public identifier;
  public isHvacOff;
  public isHeatOn;
  public isTempHold;


  constructor(private _APIService: APIService,
                private _route: ActivatedRoute) { }

  ngOnInit() {

      this.key = (this._route.snapshot.paramMap.get('key'));
      this.identifier = (this._route.snapshot.paramMap.get('identifier'));

      this.isTempHold = this.thermostat.events;
      this.isHvacOff = this.thermostat.hvacMode == 'off';
      this.isHeatOn = this.thermostat.hvacMode == 'heat';
  }

  setHvacMode(mode){
    this._APIService.setHvacMode(this.key, this.identifier, mode)
    this.isHvacOff = mode == 'off';
    this.isHeatOn = mode == 'heat';
  }

  setClimateHold(climate){
    this._APIService.setClimateHold(this.key, this.identifier, climate)
  }

  resume(){
    this._APIService.resume(this.key, this.identifier)
  }

}


          // <!--   <button class="btn btn-outline-light
          //       {% if thermostat.current_climate_data.mode == 'hold' %}
          //           active
          //       {% else %}
          //           disabled
          //       {% endif %}" style='width: 25%'>
          //       {% if thermostat.current_climate_data.endtime != 'transition' %}
          //       Hold
          //       {% else %}
          //       Reg
          //       {% endif %}
