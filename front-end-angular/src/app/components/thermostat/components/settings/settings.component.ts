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

  get isHeatOn() {
    return this.thermostat.settings.hvacMode == 'heat'
  }

  get isOnClimateHold() {
    return this.thermostat.events.length
  }

  isClimateActive(climate: any) {
    return this.thermostat.currentClimateRef == climate.climateRef
  }

  // Actions

  onSelectHvacMode(mode: string) {
    this.setHvacMode.emit(mode);
  }

  onSelectClimate(climate: any) {
    this.setClimate.emit(climate.climateRef);
  }

  onResume() {
    this.resume.emit();
  }

}
