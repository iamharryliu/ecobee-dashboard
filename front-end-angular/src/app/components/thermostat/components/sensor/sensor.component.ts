import { Component, OnInit, Input } from '@angular/core';

import { RemoteSensor } from 'app'

@Component({
  selector: 'app-sensor',
  templateUrl: './sensor.component.html',
  styleUrls: ['./sensor.component.css']
})
export class SensorComponent implements OnInit {

  @Input() public sensor: RemoteSensor;

  constructor() { }

  ngOnInit() {
  }

  getTemperature(sensor: RemoteSensor) {
    let capabilities = sensor.capability
    for (let i = 0; i < capabilities.length; i++) {
      let capability = capabilities[i]
      if (capability.type === 'temperature') {
        return this.ecobeeTempToDegrees(Number(capability.value))
      }
    }
    return false
  }

  getOccupancy(sensor: RemoteSensor) {
    let capabilities = sensor.capability
    for (let i = 0; i < capabilities.length; i++) {
      let capability = capabilities[i]
      if (capability.type === 'occupancy') {
        return capability.value == 'true'
      }
    }
  }

  getHumidity(sensor: RemoteSensor) {
    let capabilities = sensor.capability
    for (let i = 0; i < capabilities.length; i++) {
      let capability = capabilities[i]
      if (capability.type === 'humidity') {
        return capability.value
      }
    }
    return false
  }

  ecobeeTempToDegrees(temperature: number) {
    temperature = (temperature / 10 - 32) * 5 / 9
    temperature = Math.round(temperature * 10) / 10
    return temperature
  }


}
