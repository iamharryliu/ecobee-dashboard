import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API } from './api'
import { Thermostat } from './thermostat'

@Injectable({
    providedIn: 'root'
})
export class APIService {

    constructor(private http: HttpClient) { }
    getAPIS(): Observable<API[]> {
        return this.http.get<API[]>('http://localhost:5000/fetchApps')
    }

    deleteAPI(){
        console.log('delete')
    }

    getThermostats(): Observable<Thermostat[]>{
        return this.http.get<Thermostat[]>('http://localhost:5000/fetchThermostats');
    }

    getThermostat(): Observable<Thermostat[]>{
        return this.http.get<Thermostat[]>('http://localhost:5000/fetchThermostat');
    }


}

