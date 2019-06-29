import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API } from './api';
import { Thermostat } from './thermostat';

@Injectable({
    providedIn: 'root'
})
export class APIService {

    public backEndURL = 'http://localhost:5000';

    constructor(private http: HttpClient) { }

    getAPIS(): Observable<API[]> {
        return this.http.get<API[]>('http://localhost:5000/fetchAPIs')
    }

    deleteAPI(key){
        console.log('delete ' + key)
    }

    getThermostats(key): Observable<Thermostat[]>{
        return this.http.get<Thermostat[]>(`${this.backEndURL}/fetchThermostats/${key}`);
    }

    getThermostat(key, identifier): Observable<Thermostat[]>{
        return this.http.get<Thermostat[]>(`${this.backEndURL}/fetchThermostat/${key}/${identifier}`);
    }

    setHvacMode(key, identifier, mode){
        let url = `${this.backEndURL}/setHvacMode/${key}/${identifier}/${mode}`
        this.http.post(url, null).subscribe(resp => {
          console.log(resp);
        });
    }

    resume(key, identifier){
        let url = `${this.backEndURL}/resume/${key}/${identifier}`
        this.http.post(url, null).subscribe(resp => {
          console.log(resp);
        });
    }

    setClimateHold(key, identifier, climate){
        let url = `${this.backEndURL}/setClimate/${key}/${identifier}/${climate}`
        this.http.post(url, null).subscribe(resp => {
          console.log(resp);
        });
    }

    setTemperature(key, identifier, temperature){
        let url = `${this.backEndURL}/setTemperature/${key}/${identifier}/${temperature}`
        this.http.post(url, null).subscribe(resp => {
          console.log(resp);
        });
    }

    sendMessage(key, identifier, message){
        let url = `${this.backEndURL}/sendMessage/${key}/${identifier}/${message}`
        this.http.post(url, null).subscribe(resp => {
          console.log(resp);
        });
    }


}

