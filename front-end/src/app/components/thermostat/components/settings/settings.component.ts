import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { APIService } from '../../../../api.service'

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})


export class SettingsComponent implements OnInit {

  @Input() public thermostat;
  @Output() public updateThermostat: EventEmitter<void> = new EventEmitter();


  constructor(private _APIService: APIService) { }

  ngOnInit() { }

  setHvacMode(mode) {
    this.thermostat.hvacMode = mode
    this._APIService.setHvacMode(this.thermostat, mode).subscribe(resp => {
      console.log(resp);
      this.updateThermostat.emit()
    })
  }

  setClimate(climate) {
    this._APIService.setClimate(this.thermostat, climate).subscribe(resp => {
      console.log(resp);
      this.updateThermostat.emit();
    });
  }

  resume() {
    this.thermostat.currentClimateData.events = false;
    // change temperature
    // change climate
    this._APIService.resume(this.thermostat).subscribe(resp => {
      console.log(resp);
      this.updateThermostat.emit()
    });
  }

}
