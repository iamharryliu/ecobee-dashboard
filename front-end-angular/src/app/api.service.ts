import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const httpOptions = {
    withCredentials: true,
};

@Injectable({
    providedIn: 'root'
})
export class APIService {

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

    deleteApp(api_key): Observable<any> {
        return this.http.delete<any>(`${this.backEndURL}/apps/delete/${api_key}`)
    }

    // Thermostats

    getUserThermostats(): Observable<any> {
        return this.http.get<any>(`${this.backEndURL}/getUserThermostats`, httpOptions);
    }

    getThermostat(thermostat): Observable<any> {
        let identifier = thermostat.identifier;
        return this.http.get<any>(`${this.backEndURL}/thermostat/${identifier}`, httpOptions);
    }

    getThermostatRuntimeReport(): Observable<any> {
        return this.http.get<any>(`${this.backEndURL}/runtimeReport`, httpOptions);
    }

    // Thermostat Actions

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

