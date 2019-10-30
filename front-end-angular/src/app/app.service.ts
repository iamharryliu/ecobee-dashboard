import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { App } from 'app';

const httpOptions = { withCredentials: true };

@Injectable()
export class AppService {

  constructor(private http: HttpClient) { }

  public backEndURL = 'http://localhost:8000';
  public url = `${this.backEndURL}/apps`

  // Ecobee App

  getEcobeeServerStatus(): Observable<any> {
    return this.http.get<any>(`${this.url}/checkAPI`, httpOptions)
  }

  authorizeApp(key: string): Observable<any> {
    return this.http.get<any>(`${this.url}/authorize/${key}`, httpOptions)
  }

  createApp(form: any): Observable<any> {
    return this.http.post<any>(`${this.url}/create`, form, httpOptions)
  }

  updateAppCredentials(key: string, authorization_code: string): Observable<any> {
    let form = {
      'api_key': key,
      'authorization_code': authorization_code
    }
    return this.http.post<any>(`${this.url}/updateCredentials`, form, httpOptions)
  }

  getApps(): Observable<any> {
    return this.http.get<any>(`${this.url}`, httpOptions)
  }

  deleteApp(key: string): Observable<any> {
    return this.http.delete<any>(`${this.url}/delete/${key}`)
  }

  // Thermostat

  getUserThermostats(): Observable<App[]> {
    return this.http.get<App[]>(`${this.url}/getUserThermostats`, httpOptions);
  }

  getAppThermostats(key: string): Observable<App[]> {
    return this.http.get<App[]>(`${this.url}/getAppThermostats/${key}`, httpOptions)
  }

  getThermostat(identifier: string): Observable<any> {
    return this.http.get<App>(`${this.url}/thermostat/${identifier}`, httpOptions);
  }

  getThermostatRuntimeReport(thermostat: App): Observable<any> {
    let key = thermostat.api_key;
    let identifier = thermostat.data.identifier;
    return this.http.get<any>(`${this.url}/thermostats/${key}/${identifier}/runtimeReport`, httpOptions);
  }

  // Thermostat Actions

  setHvacMode(thermostat: App, mode: string): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier,
      mode: mode
    }
    let url = `${this.url}/setHvacMode`
    return this.http.post(url, data)
  }

  resume(thermostat: App): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier
    }
    let url = `${this.url}/resume`
    return this.http.post<any>(url, data)
  }

  setClimate(thermostat: App, climate: string): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier,
      climate: climate
    }
    let url = `${this.url}/setClimate`
    return this.http.post(url, data)
  }

  setTemperature(thermostat: App, temperature: number): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier,
      temperature: temperature
    }
    let url = `${this.url}/setTemperature`
    return this.http.post(url, data);
  }

  sendMessage(thermostat: App, message: string): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier,
      message: message
    }
    let url = `${this.url}/sendMessage`
    return this.http.post(url, data)
  }

}
