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

    getThermostat(key, identifier): Observable<any> {
        return this.http.get<any>(`${this.backEndURL}/fetchThermostat/${key}/${identifier}`);
    }

    setHvacMode(thermostat, mode): Observable<any> {
        let url = `${this.backEndURL}/setHvacMode/${thermostat.key}/${thermostat.identifier}/${mode}`
        return this.http.post(url, null)
    }

    resume(thermostat): Observable<any> {
        let url = `${this.backEndURL}/resume/${thermostat.key}/${thermostat.identifier}`
        return this.http.post(url, null)
    }

    setClimate(thermostat, climate): Observable<any> {
        let url = `${this.backEndURL}/setClimate/${thermostat.key}/${thermostat.identifier}/${climate}`
        return this.http.post(url, null)
    }

    setTemperature(thermostat, temperature): Observable<any> {
        let url = `${this.backEndURL}/setTemperature/${thermostat.key}/${thermostat.identifier}/${temperature}`
        return this.http.post(url, null);
    }

    sendMessage(key, identifier, message): Observable<any> {
        let url = `${this.backEndURL}/sendMessage/${key}/${identifier}/${message}`
        return this.http.post(url, null)
    }


}

