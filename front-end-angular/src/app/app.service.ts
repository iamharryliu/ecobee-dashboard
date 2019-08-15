import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Thermostat } from '../../app';

const httpOptions = {
  withCredentials: true,
};

@Injectable({
  providedIn: 'root'
})
export class AppService {

  public backEndURL = 'http://localhost:5000';

  constructor(private http: HttpClient) { }

  // Apps

  authorizeApp(apiKey: string): Observable<any> {
    return this.http.get<any>(`${this.backEndURL}/apps/authorize/${apiKey}`, httpOptions)
  }

  createApp(form: any): Observable<any> {
    return this.http.post<any>(`${this.backEndURL}/apps/create`, form, httpOptions)
  }

  updateAppCredentials(api_key: string, authorization_code: string): Observable<any> {
    let form = {
      'api_key': api_key,
      'authorization_code': authorization_code
    }
    return this.http.post<any>(`${this.backEndURL}/apps/updateAppCredentials`, form, httpOptions)
  }

  getApps(): Observable<any> {
    return this.http.get<any>(`${this.backEndURL}/apps`, httpOptions)
  }

  deleteApp(api_key: string): Observable<any> {
    return this.http.delete<any>(`${this.backEndURL}/apps/delete/${api_key}`)
  }

  // Thermostats

  getUserThermostats(): Observable<Thermostat[]> {
    return this.http.get<Thermostat[]>(`${this.backEndURL}/getUserThermostats`, httpOptions);
  }

  getThermostat(thermostat: Thermostat): Observable<any> {
    let identifier = thermostat.data.identifier;
    return this.http.get<Thermostat>(`${this.backEndURL}/thermostat/${identifier}`, httpOptions);
  }

  getThermostatRuntimeReport(thermostat: Thermostat): Observable<any> {
    let identifier = thermostat.data.identifier;
    return this.http.get<any>(`${this.backEndURL}/thermostats/${identifier}/runtimeReport`, httpOptions);
  }

  // Thermostat Actions

  setHvacMode(thermostat: Thermostat, mode: string): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier,
      mode: mode
    }
    let url = `${this.backEndURL}/setHvacMode`
    return this.http.post(url, data)
  }

  resume(thermostat: Thermostat): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier
    }
    let url = `${this.backEndURL}/resume`
    return this.http.post<any>(url, data)
  }

  setClimate(thermostat: Thermostat, climate: string): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier,
      climate: climate
    }
    let url = `${this.backEndURL}/setClimate`
    return this.http.post(url, data)
  }

  setTemperature(thermostat: Thermostat, temperature: number): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier,
      temperature: temperature
    }
    let url = `${this.backEndURL}/setTemperature`
    return this.http.post(url, data);
  }

  sendMessage(thermostat: Thermostat, message: string): Observable<any> {
    let data = {
      key: thermostat.api_key,
      identifier: thermostat.data.identifier,
      message: message
    }
    let url = `${this.backEndURL}/sendMessage`
    return this.http.post(url, data)
  }


}
