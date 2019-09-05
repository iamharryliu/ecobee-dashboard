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
  public backEndURL = 'http://localhost:5000';

  setLoginStatus(status: boolean) {
    this.loginStatus = status
  }

  getLoginStatus(): Observable<any> {
    return this.http.get<any>(`${this.backEndURL}/getLoggedInStatus`, httpOptions)
  }

  registerUser(data: any): Observable<any> {
    return this.http.post<any>(`${this.backEndURL}/registerUser`, data, httpOptions)
  }

  loginUser(data: any): Observable<any> {
    return this.http.post<any>(`${this.backEndURL}/loginUser`, data, httpOptions)
  }

  logoutUser(): Observable<any> {
    return this.http.post<any>(`${this.backEndURL}/logoutUser`, null, httpOptions)
  }

}
