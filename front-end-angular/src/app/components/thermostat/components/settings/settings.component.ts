import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

import { AppService } from '../../../../app.service'

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})


export class SettingsComponent implements OnInit {

  @Input() public thermostat: any;
  @Output() public updateThermostat: EventEmitter<void> = new EventEmitter();

  constructor(private _AppService: AppService) { }

  ngOnInit() { }

  get isHeatOn() { return this.thermostat.data.settings.hvacMode == 'heat' }
  get isOnClimateHold() { return this.thermostat.data.events.length }
  isClimateActive(climate: any) { return this._AppService.getCurrentClimateRef(this.thermostat) == climate.climateRef }

  // Thermostat actions.

  onSelectHvacMode(mode: string) {
    this.thermostat.hvacMode = mode
    this._AppService.setHvacMode(this.thermostat, mode).subscribe(_ => {
      console.log('Successfully set HVAC mode.');
      this.updateThermostat.emit()
    })
  }

  onSelectClimate(climate: any) {
    this._AppService.setClimate(this.thermostat, climate).subscribe(_ => {
      console.log('Successfully set climate.');
      this.updateThermostat.emit();
    });
  }

  onResume() {
    this._AppService.resume(this.thermostat).subscribe(_ => {
      console.log('Successfully resumed thermostat program.');
      this.updateThermostat.emit()
    });
  }

}
