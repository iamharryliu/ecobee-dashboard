import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { APIService } from '../../../../api.service';

@Component({
  selector: 'app-temperature',
  templateUrl: './temperature.component.html',
  styleUrls: ['./temperature.component.css']
})
export class TemperatureComponent implements OnInit {

  @Input() public thermostat;
  @Output() public updateThermostat: EventEmitter<void> = new EventEmitter();

  public temperatureOptions = [18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0];

  constructor(private _APIService: APIService) { }

  ngOnInit() { }

  setTemperature(temperature) {
    this._APIService.setTemperature(this.thermostat, temperature).subscribe(resp => {
      console.log(resp);

      this.updateThermostat.emit()
    });
  }

}
