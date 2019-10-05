import { Component, OnInit, Input, OnDestroy } from '@angular/core';
import * as Highstock from 'highcharts/highstock';
import { AppService } from '../../../../app.service'
import { Subscription } from 'rxjs';

declare var require: any;

let noData = require('highcharts/modules/no-data-to-display');
let HC_exporting = require('highcharts/modules/exporting')
let HC_export_data = require('highcharts/modules/export-data')
let theme = require('highcharts/themes/sand-signika')
noData(Highstock);
HC_exporting(Highstock);
HC_export_data(Highstock);
theme(Highstock);

@Component({
  selector: 'app-weather-chart',
  templateUrl: './weather-chart.component.html',
  styleUrls: ['./weather-chart.component.css']
})
export class WeatherChartComponent implements OnInit, OnDestroy {

  @Input() public thermostat: any;
  public runtimeReport: any;
  public runtimeReportSub: Subscription;
  public options: any;
  public series = [];

  constructor(private _AppService: AppService) { }

  ngOnInit() {

    this.setOptions()
    Highstock.stockChart('container', this.options);

    this.runtimeReportSub = this._AppService.getThermostatRuntimeReport(this.thermostat).subscribe(data => {

      let outdoorTempSeries = [];
      let zoneAveTempSeries = [];
      let zoneHeatTempSeries = [];
      let outdoorHumiditySeries = [];
      let zoneHumiditySeries = [];

      let columns = data.columns.split(',')

      let hvacModeIndex = columns.indexOf('HVACmode') + 2
      // let zoneCalendarEventIndex = columns.indexOf('zoneCalendarEvent') + 2
      // let zoneOccupancyIndex = columns.indexOf('zoneOccupancy') + 2
      let outdoorTempIndex = columns.indexOf('outdoorTemp') + 2
      let zoneAveTempIndex = columns.indexOf('zoneAveTemp') + 2
      let zoneHeatTempIndex = columns.indexOf('zoneHeatTemp') + 2
      // let zoneCoolTempIndex = columns.indexOf('zoneCoolTemp') + 2
      let outdoorHumidityIndex = columns.indexOf('outdoorHumidity') + 2
      let zoneHumidityIndex = columns.indexOf('zoneHumidity') + 2

      let rowList = data.reportList[0].rowList

      for (let i = 0; i < rowList.length; i++) {

        let rowData = rowList[i].split(',')

        let datetime = rowData[0] + ' ' + rowData[1] + ' GMT'
        let time = Date.parse(datetime)

        if (rowData[hvacModeIndex]) {

          let outdoorTemp = rowData[outdoorTempIndex]
          let zoneAveTemp = rowData[zoneAveTempIndex]
          let zoneHeatTemp = rowData[zoneHeatTempIndex]
          let outdoorHumidity = rowData[outdoorHumidityIndex]
          let zoneHumidity = rowData[zoneHumidityIndex]

          outdoorTemp = (outdoorTemp - 32) * 5 / 9
          zoneAveTemp = (zoneAveTemp - 32) * 5 / 9
          zoneHeatTemp = (zoneHeatTemp - 32) * 5 / 9
          outdoorHumidity = parseInt(outdoorHumidity)
          zoneHumidity = parseInt(zoneHumidity)

          rowData.splice(outdoorTempIndex, 1, outdoorTemp)
          rowData.splice(zoneAveTempIndex, 1, zoneAveTemp)
          rowData.splice(zoneHeatTempIndex, 1, zoneHeatTemp)
          rowData.splice(outdoorHumidityIndex, 1, outdoorHumidity)
          rowData.splice(zoneHumidityIndex, 1, zoneHumidity)
          rowData.splice(0, 2, time)
          // if (rowData[0] % (30 * 60 * 1000) == 0) {
          //   outdoorTempSeries.push([rowData[0], rowData[outdoorTempIndex - 1]])
          //   outdoorHumiditySeries.push([rowData[0], rowData[outdoorHumidityIndex - 1]])
          // }
          outdoorTempSeries.push([rowData[0], rowData[outdoorTempIndex - 1]])
          outdoorHumiditySeries.push([rowData[0], rowData[outdoorHumidityIndex - 1]])
          zoneAveTempSeries.push([rowData[0], rowData[zoneAveTempIndex - 1]])
          zoneHeatTempSeries.push([rowData[0], rowData[zoneHeatTempIndex - 1]])
          zoneHumiditySeries.push([rowData[0], rowData[zoneHumidityIndex - 1]])
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

  ngOnDestroy() {
    if (this.runtimeReportSub) {
      this.runtimeReportSub.unsubscribe()
    }
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
          type: 'day',
          count: 7,
          text: '7d'
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