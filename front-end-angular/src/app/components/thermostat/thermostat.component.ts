import { Component, OnInit } from '@angular/core';
import { APIService } from '../../api.service'
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-thermostat',
  templateUrl: './thermostat.component.html',
  styleUrls: ['./thermostat.component.css']
})
export class ThermostatComponent implements OnInit {

  public thermostat: any;
  public thermostatSensor: any;
  public remoteSensors: any;
  public all_data_fetched = false;
  public runtimeReport: any;

  constructor(private _APIService: APIService,
    private _route: ActivatedRoute) { }

  ngOnInit() {
    let key = (this._route.snapshot.paramMap.get('key'));
    let identifier = (this._route.snapshot.paramMap.get('identifier'));
    this.thermostat = { key: key, identifier: identifier }
    this.updateThermostat()
    this._APIService.getThermostatRuntimeReport().subscribe(data => {
      this.runtimeReport = data
      let reportColumnList = this.getReportColumnList()
      let sensorColumnList = this.getSensorColumnList()
      console.log(reportColumnList)
      console.log(sensorColumnList)
    })
  }

  getReportColumnList() {
    let rowList = this.runtimeReport.reportList[0]['rowList']
    let columnList = [];
    let numberOfColumns = this.runtimeReport.columns.split(',').length + 2
    for (let i = 0; i < numberOfColumns; i++) {
      columnList.push([])
    }
    for (let rowIndex = 0; rowIndex < rowList.length; rowIndex++) {
      rowList[rowIndex] = rowList[rowIndex].split(',')
      for (let colIndex = 0; colIndex < numberOfColumns; colIndex++) {
        columnList[colIndex].push(rowList[rowIndex][colIndex])
      }
    }
    return columnList
  }

  getSensorColumnList() {
    let rowList = this.runtimeReport.sensorList[0].data
    let columnList = [];
    let numberOfColumns = this.runtimeReport.sensorList[0].columns.length
    for (let i = 0; i < numberOfColumns; i++) {
      columnList.push([])
    }
    for (let rowIndex = 0; rowIndex < rowList.length; rowIndex++) {
      rowList[rowIndex] = rowList[rowIndex].split(',')
      for (let colIndex = 0; colIndex < numberOfColumns; colIndex++) {
        columnList[colIndex].push(rowList[rowIndex][colIndex])
      }
    }
    return columnList
  }

  updateThermostat() {
    this._APIService.getThermostat(this.thermostat)
      .subscribe(data => {
        this.thermostat = data;
        this.remoteSensors = this.thermostat.remoteSensors;
        this.reserializeThermostatData();
        this.all_data_fetched = true;
      });
  }

  reserializeThermostatData() {
    this.reserializeSensors()
    this.reserializeActualTemperature()
    this.reserializeClimateData()
  }

  reserializeActualTemperature() {
    this.thermostat.actualTemperature = this.ecobeeTempToDegrees(this.thermostat.runtime.actualTemperature)
  }

  reserializeClimateData() {
    this.thermostat.currentClimateRef = this.currentClimateRef
    this.thermostat.currentClimateRefTemp = this.currentClimateRefTemp
  }

  get currentClimateRef() {
    var currentClimateRef: string;
    if (this.thermostat.events.length) {
      if (this.thermostat.events[0].holdClimateRef == '') {
        currentClimateRef = 'hold'
      }
      else {
        currentClimateRef = this.thermostat.events[0].holdClimateRef
      }
    }
    else {
      currentClimateRef = this.thermostat.program.currentClimateRef
    }
    return currentClimateRef
  }

  get currentClimateRefTemp() {
    var temperature: number
    if (this.thermostat.events.length) {
      temperature = this.thermostat.events[0].heatHoldTemp
    }
    else {
      for (let climate of this.thermostat.program.climates) {
        if (this.currentClimateRef == climate.climateRef) {
          temperature = climate.heatTemp
        }
      }
    }
    return this.ecobeeTempToDegrees(temperature)
  }

  reserializeSensors() {
    for (let i = 0; i < this.remoteSensors.length; i++) {
      let remoteSensor = this.remoteSensors[i]
      if (remoteSensor.type == 'ecobee3_remote_sensor') {
        remoteSensor.type = 'remote sensor'
      }
      let capabilities = remoteSensor.capability
      for (let j = 0; j < capabilities.length; j++) {
        let capability = capabilities[j]
        if (capability.type == 'temperature') {
          remoteSensor.temperature = this.ecobeeTempToDegrees(capability.value)
        }
        if (capability.type == 'humidity') {
          remoteSensor.humidity = capability.value
        }
        if (capability.type == 'occupancy') {
          remoteSensor.occupancy = capability.value == 'true'
        }
      }
    }
    this.remoteSensors.sort((b: string, a: string) => (a > b ? 1 : -1));
  }

  // Thermostat Actions

  setTemperature(temperature: string) {
    this._APIService.setTemperature(this.thermostat, temperature).subscribe(response => {
      console.log(response);
      this.updateThermostat()
    });
  }

  setHvacMode(mode: string) {
    this.thermostat.hvacMode = mode
    this._APIService.setHvacMode(this.thermostat, mode).subscribe(response => {
      console.log(response);
      this.updateThermostat()
    })
  }

  setClimate(climate: string) {
    this._APIService.setClimate(this.thermostat, climate).subscribe(response => {
      console.log(response);
      this.updateThermostat();
    });
  }

  resume() {
    this._APIService.resume(this.thermostat).subscribe(response => {
      console.log(response);
      this.updateThermostat()
    });
  }

  // Utility

  ecobeeTempToDegrees(temperature: number) {
    temperature = (temperature / 10 - 32) * 5 / 9
    temperature = Math.round(temperature * 10) / 10
    return temperature
  }

}
