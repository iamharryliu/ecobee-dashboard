import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const httpOptions = {
  withCredentials: true,
};

@Injectable()
export class UserService {

  constructor(private http: HttpClient) { }

  public loginStatus = false;
  public backEndURL = 'http://localhost:8000';
  public url = `${this.backEndURL}/users`


  getLoginStatus(): Observable<any> {
    return this.http.get<any>(`${this.url}/loginStatus`, httpOptions)
  }

  setLoginStatus(status: boolean) {
    this.loginStatus = status
  }

  registerUser(data: any): Observable<any> {
    return this.http.post<any>(`${this.url}/register`, data, httpOptions)
  }

  loginUser(data: any): Observable<any> {
    return this.http.post<any>(`${this.url}/login`, data, httpOptions)
  }

  logoutUser(): Observable<any> {
    return this.http.post<any>(`${this.url}/logout`, null, httpOptions)
  }

}
