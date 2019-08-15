import { Component, OnInit, Input } from '@angular/core';
import * as Highstock from 'highcharts/highstock';
import { AppService } from '../../../../app.service'

declare var require: any;

let noData = require('highcharts/modules/no-data-to-display');
let HC_exporting = require('highcharts/modules/exporting')
let HC_export_data = require('highcharts/modules/export-data')
// let Boost = require('highcharts/modules/boost');

noData(Highstock);
HC_exporting(Highstock);
HC_export_data(Highstock);
// Boost(Highstock);


@Component({
  selector: 'app-weather-chart',
  templateUrl: './weather-chart.component.html',
  styleUrls: ['./weather-chart.component.css']
})
export class WeatherChartComponent implements OnInit {

  @Input() public thermostat: any;
  public runtimeReport: any;
  public options: any;
  public series = [];

  constructor(private _AppService: AppService) { }

  ngOnInit() {
    // let utcTime = this.thermostat.data.utcTime

    this._AppService.getThermostatRuntimeReport(this.thermostat).subscribe(data => {

      let outdoorTempSeries = [];
      let zoneAveTempSeries = [];
      let zoneHeatTempSeries = [];
      let outdoorHumiditySeries = [];
      let zoneHumiditySeries = [];

      let hvacModeIndex = data.columns.split(',').indexOf('HVACmode') + 2
      let zoneCalendarEventIndex = data.columns.split(',').indexOf('zoneCalendarEvent') + 2
      let zoneOccupancyIndex = data.columns.split(',').indexOf('zoneOccupancy') + 2
      let outdoorTempIndex = data.columns.split(',').indexOf('outdoorTemp') + 2
      let zoneAveTempIndex = data.columns.split(',').indexOf('zoneAveTemp') + 2
      let zoneHeatTempIndex = data.columns.split(',').indexOf('zoneHeatTemp') + 2
      let zoneCoolTempIndex = data.columns.split(',').indexOf('zoneCoolTemp') + 2
      let outdoorHumidityIndex = data.columns.split(',').indexOf('outdoorHumidity') + 2
      let zoneHumidityIndex = data.columns.split(',').indexOf('zoneHumidity') + 2

      let rowList = data.reportList[0].rowList
      for (let i = 0; i < rowList.length; i++) {
        rowList[i] = rowList[i].split(',')
        let datetime = rowList[i][0] + ' ' + rowList[i][1] + ' GMT'
        let time = Date.parse(datetime)
        if (rowList[i][hvacModeIndex]) {
          let outdoorTemp = rowList[i][outdoorTempIndex]
          let zoneAveTemp = rowList[i][zoneAveTempIndex]
          let zoneHeatTemp = rowList[i][zoneHeatTempIndex]
          let outdoorHumidity = rowList[i][outdoorHumidityIndex]
          let zoneHumidity = rowList[i][zoneHumidityIndex]
          outdoorTemp = (outdoorTemp - 32) * 5 / 9
          zoneAveTemp = (zoneAveTemp - 32) * 5 / 9
          zoneHeatTemp = (zoneHeatTemp - 32) * 5 / 9
          outdoorHumidity = parseInt(outdoorHumidity)
          zoneHumidity = parseInt(zoneHumidity)
          rowList[i].splice(outdoorTempIndex, 1, outdoorTemp)
          rowList[i].splice(zoneAveTempIndex, 1, zoneAveTemp)
          rowList[i].splice(zoneHeatTempIndex, 1, zoneHeatTemp)
          rowList[i].splice(outdoorHumidityIndex, 1, outdoorHumidity)
          rowList[i].splice(zoneHumidityIndex, 1, zoneHumidity)
          rowList[i].splice(0, 2, time)
          if (rowList[i][0] % (30 * 60 * 1000) == 0) {
            outdoorTempSeries.push([rowList[i][0], rowList[i][outdoorTempIndex - 1]])
            outdoorHumiditySeries.push([rowList[i][0], rowList[i][outdoorHumidityIndex - 1]])
          }
          zoneAveTempSeries.push([rowList[i][0], rowList[i][zoneAveTempIndex - 1]])
          zoneHeatTempSeries.push([rowList[i][0], rowList[i][zoneHeatTempIndex - 1]])
          zoneHumiditySeries.push([rowList[i][0], rowList[i][zoneHumidityIndex - 1]])
        }
      }
      let sensorList = data.sensorList[0]
      let sensorListData = sensorList.data
      let sensors = sensorList.sensors
      for (let i = 0; i < sensors.length; i++) {
        sensors[i].data = []
      }
      for (let i = 0; i < sensorListData.length; i++) {
        sensorListData[i] = sensorListData[i].split(',')
        let datetime = sensorListData[i][0] + ' ' + sensorListData[i][1] + ' GMT'
        let time = Date.parse(datetime)
        if (sensorListData[i][2] != 'null') {
          for (let j = 0; j < sensors.length; j++) {
            if (sensors[j].sensorType == 'temperature' || sensors[j].sensorType == 'humidity') {
              data = parseFloat(sensorListData[i][j + 2])
              if (sensors[j].sensorType == 'temperature') {

                data = (data - 32) * 5 / 9
              }
            }
            else {
              data = sensorListData[i][j + 2]
            }
            sensors[j].data.push([time, data])

          }
        }
      }
      for (let i = 0; i < sensors.length; i++) {
        let sensor = sensors[i]
        if (sensor.sensorType == 'temperature') {
          this.series.push({
            name: sensor.sensorName,
            type: 'spline',
            yAxis: 0,
            data: sensor.data,
            visible: true
          })
        }
        if (sensor.sensorType == 'humidity') {
          this.series.push({
            name: sensor.sensorName,
            type: 'spline',
            yAxis: 1,
            data: sensor.data,
            visible: false
          })
        }
      }
      this.series.push({
        name: 'Outdoor Temp',
        type: 'spline',
        yAxis: 0,
        data: outdoorTempSeries,
        visible: false
      })
      this.series.push({
        name: 'Outdoor Humidity',
        type: 'spline',
        yAxis: 1,
        data: outdoorHumiditySeries,
        visible: false
      })
      this.series.push({
        name: 'Zone Ave Temp',
        type: 'spline',
        yAxis: 0,
        data: zoneAveTempSeries,
        visible: false
      })
      this.series.push({
        name: 'Zone Heat Temp',
        type: 'spline',
        yAxis: 0,
        data: zoneHeatTempSeries,
        visible: false
      })
      this.series.push({
        name: 'Zone Humidity',
        type: 'spline',
        yAxis: 1,
        data: zoneHumiditySeries,
        visible: false
      })

      this.setOptions()
      Highstock.stockChart('container', this.options);
    })
  }
  setOptions() {
    this.options = {
      chart: {
        height: 500,
        zoomType: 'x',
      },
      title: {
        text: 'Weather Chart'
      },
      subtitle: {
        text: 'Temperature, Humidity, Climate Setting'
      },
      xAxis: {
        type: 'datetime',
      },
      yAxis: [
        {
          title: {
            text: 'Temperature'
          },
          opposite: false
        },
        {
          title: {
            text: 'Humidity'
          },
        },
      ],
      series: this.series,
      rangeSelector: {
        selected: 5,
        buttons: [{
          type: 'hour',
          count: 4,
          text: '4h'
        }, {
          type: 'hour',
          count: 6,
          text: '6h'
        }, {
          type: 'hour',
          count: 12,
          text: '12h'
        }, {
          type: 'day',
          count: 1,
          text: '1d'
        }, {
          type: 'day',
          count: 3,
          text: '3d'
        }, {
          type: 'week',
          count: 1,
          text: '1w'
        }, {
          type: 'all',
          text: 'All'
        }]
      },
      tooltip: {
        pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
        valueDecimals: 2,
        split: false,
        shared: true
      },
      credits: {
        enabled: false
      },
      legend: {
        enabled: true
      },
    }
  }
}