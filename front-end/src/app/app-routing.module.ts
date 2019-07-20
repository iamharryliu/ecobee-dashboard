import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { NavbarComponent } from './components/layout/navbar/navbar.component';
import { MainComponent } from './components/main/main.component';

import { AppsComponent } from './components/apps/apps.component';

import { RegisterUserComponent } from './components/register-user/register-user.component';
import { LoginComponent } from './components/login/login.component';

import { RegisterApiComponent } from './components/register-api/register-api.component';
import { ThermostatsComponent } from './components/thermostats/thermostats.component'
import { ThermostatComponent } from './components/thermostat/thermostat.component';
import { TemperatureComponent } from './components/thermostat/components/temperature/temperature.component';
import { SettingsComponent } from './components/thermostat/components/settings/settings.component';
import { SensorComponent } from './components/thermostat/components/sensor/sensor.component';
import { MessageComponent } from './components/thermostat/components/message/message.component';

import { AuthGuard } from './auth.guard'

const routes: Routes = [

  { path: '', component: MainComponent },

  { path: 'login', component: LoginComponent },
  { path: 'registerUser', component: RegisterUserComponent },

  { path: 'register_api', component: RegisterApiComponent },
  { path: 'apps', component: AppsComponent, canActivate: [AuthGuard] },

  { path: 'apis/:key', component: ThermostatsComponent },
  { path: 'apis/:key/:identifier', component: ThermostatComponent }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const RoutingComponents = [MainComponent,
  NavbarComponent,
  AppsComponent,
  RegisterUserComponent,
  LoginComponent,
  RegisterApiComponent,
  ThermostatsComponent,
  ThermostatComponent,
  TemperatureComponent,
  SettingsComponent,
  SensorComponent,
  MessageComponent,]
