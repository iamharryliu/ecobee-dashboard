import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Thermostat } from '../../app';

const httpOptions = {
  withCredentials: true,
};

@Injectable()
export class AppService {

  constructor(private http: HttpClient) { }

  public backEndURL = 'http://localhost:8000';
  public url = `${this.backEndURL}/apps`

  // Ecobee App

  checkAPI(): Observable<any> {
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

  getUserThermostats(): Observable<Thermostat[]> {
    return this.http.get<Thermostat[]>(`${this.url}/getUserThermostats`, httpOptions);
  }

  getAppThermostats(key: string): Observable<Thermostat[]> {
    return this.http.get<Thermostat[]>(`${this.url}/getAppThermostats/${key}`, httpOptions)
  }

  getThermostat(thermostat: Thermostat): Observable<any> {
    let identifier = thermostat.data.identifier;
    return this.http.get<Thermostat>(`${this.url}/thermostat/${identifier}`, httpOptions);
  }

  getThermostatRuntimeReport(thermostat: Thermostat): Observable<any> {
    let key = thermostat.api_key;
    let identifier = thermostat.data.identifier;
    return this.http.get<any>(`${this.url}/thermostats/${key}/${identifier}/runtimeReport`, httpOptions);
  }

  // Thermostat Actions

  setHvacMode(thermostat: Thermostat, mode: string): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier,
      mode: mode
    }
    let url = `${this.url}/setHvacMode`
    return this.http.post(url, data)
  }

  resume(thermostat: Thermostat): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier
    }
    let url = `${this.url}/resume`
    return this.http.post<any>(url, data)
  }

  setClimate(thermostat: Thermostat, climate: string): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier,
      climate: climate
    }
    let url = `${this.url}/setClimate`
    return this.http.post(url, data)
  }

  setTemperature(thermostat: Thermostat, temperature: number): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier,
      temperature: temperature
    }
    let url = `${this.url}/setTemperature`
    return this.http.post(url, data);
  }

  sendMessage(thermostat: Thermostat, message: string): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier,
      message: message
    }
    let url = `${this.url}/sendMessage`
    return this.http.post(url, data)
  }

}
