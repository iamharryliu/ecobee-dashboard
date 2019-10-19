import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { AppService } from 'src/app/app.service'
import { ThermostatService } from 'src/app/thermostat.service';

@Component({
  selector: 'app-temperature',
  templateUrl: './temperature.component.html',
  styleUrls: ['./temperature.component.css']
})
export class TemperatureComponent implements OnInit {

  @Input() public thermostat: any;
  @Input() public currentClimateRefTemp: number;
  @Output() public updateThermostat: EventEmitter<string> = new EventEmitter();

  public temperatureOptions = [18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0];

  constructor(
    private _AppService: AppService,
    private _ThermostatService: ThermostatService
  ) { }

  ngOnInit() { }

  get actualTemperature() { return this._ThermostatService.ecobeeTempToDegrees(this.thermostat.data.runtime.actualTemperature) }
  get climateRef() { return this._ThermostatService.getCurrentClimateRef(this.thermostat) }

  // Thermostat actions.

  setTemperature(temperature: string) {
    this._AppService.setTemperature(this.thermostat, parseFloat(temperature)).subscribe(_ => {
      console.log('Successfully set temperature.');
      this.updateThermostat.emit()
    });
  }

}
