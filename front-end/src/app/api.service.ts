import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
    providedIn: 'root'
})
export class APIService {

    public backEndURL = 'http://localhost:5000';

    constructor(private http: HttpClient) { }

    getAPIS(): Observable<any> {
        return this.http.get<any>('http://localhost:5000/fetchAPIs')
    }

    deleteAPI(key) {
        console.log('delete ' + key)
    }

    getThermostats(key): Observable<any> {
        return this.http.get<any>(`${this.backEndURL}/fetchThermostats/${key}`);
    }

    getThermostat(thermostat): Observable<any> {
        let key = thermostat.key;
        let identifier = thermostat.identifier;
        return this.http.get<any>(`${this.backEndURL}/fetchThermostat/${key}/${identifier}`);
    }

    setHvacMode(thermostat, mode): Observable<any> {
        let data = {
            key: thermostat.key,
            identifier: thermostat.identifier,
            mode: mode
        }
        let url = `${this.backEndURL}/setHvacMode`
        return this.http.post(url, data)
    }

    resume(thermostat): Observable<any> {
        let data = {
            key: thermostat.key,
            identifier: thermostat.identifier
        }
        let url = `${this.backEndURL}/resume`
        return this.http.post<any>(url, data)
    }

    setClimate(thermostat, climate): Observable<any> {
        let data = {
            key: thermostat.key,
            identifier: thermostat.identifier,
            climate: climate
        }
        let url = `${this.backEndURL}/setClimate`
        return this.http.post(url, data)
    }

    setTemperature(thermostat, temperature): Observable<any> {
        let data = {
            key: thermostat.key,
            identifier: thermostat.identifier,
            temperature: temperature
        }
        let url = `${this.backEndURL}/setTemperature`
        return this.http.post(url, data);
    }

    sendMessage(thermostat, message): Observable<any> {
        let data = {
            key: thermostat.key,
            identifier: thermostat.identifier,
            message: message
        }
        let url = `${this.backEndURL}/sendMessage`
        return this.http.post(url, data)
    }


}

