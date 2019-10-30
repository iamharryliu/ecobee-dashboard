import { Component, OnInit, Input } from '@angular/core';
import { ThermostatService } from 'src/app/thermostat.service';
import { RemoteSensor, Capability } from 'app'

@Component({
  selector: 'app-sensor',
  templateUrl: './sensor.component.html',
  styleUrls: ['./sensor.component.css']
})
export class SensorComponent implements OnInit {

  @Input() public sensor: RemoteSensor;

  constructor(private _ThermostatService: ThermostatService) { }

  ngOnInit() { }

  getTemperature(sensor: RemoteSensor) {
    let capabilities = sensor.capability
    let capability = capabilities.find((capability) => this.isTemperature(capability))
    return this._ThermostatService.ecobeeTempToDegrees(Number(capability.value))
  }

  getOccupancy(sensor: RemoteSensor) {
    let capabilities = sensor.capability
    let capability = capabilities.find((capability) => this.isOccupancy(capability))
    return capability.value == 'true'
  }

  getHumidity(sensor: RemoteSensor) {
    let capabilities = sensor.capability
    let capability = capabilities.find((capability) => this.isHumidity(capability))
    return capability.value
  }

  isTemperature = (capability: Capability) => capability.type === 'temperature'
  isOccupancy = (capability: Capability) => capability.type === 'occupancy'
  isHumidity = (capability: Capability) => capability.type === 'humidity'

}
