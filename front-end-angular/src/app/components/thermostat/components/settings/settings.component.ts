import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})


export class SettingsComponent implements OnInit {

  @Input() public thermostat: any;
  @Output() public setHvacMode: EventEmitter<string> = new EventEmitter();
  @Output() public setClimate: EventEmitter<string> = new EventEmitter();
  @Output() public resume: EventEmitter<void> = new EventEmitter();


  constructor() { }

  ngOnInit() { }

  isHeatOn() {
    return this.thermostat.hvacMode == 'heat'
  }

  isOnClimateHold() {
    return this.thermostat.currentClimateData.events
  }

  isClimateActive(climate: string) {
    return this.thermostat.currentClimateData.mode == climate
  }

  onSelectClimate(climate: string) {
    this.setClimate.emit(climate);
  }

  onSelectHvacMode(mode: string) {
    this.setHvacMode.emit(mode);
  }

  onResume() {
    this.resume.emit();
  }


}
