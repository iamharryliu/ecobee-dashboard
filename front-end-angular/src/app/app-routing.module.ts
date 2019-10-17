import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Main Components
import { MainComponent } from './components/main/main.component';
import { NavbarComponent } from './components/layout/navbar/navbar.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

// User Components
import { RegisterUserComponent } from './components/register-user/register-user.component';
import { LoginComponent } from './components/login/login.component';

// App Components
import { AppsComponent } from './components/apps/apps.component';
import { RegisterAppComponent } from './components/register-app/register-app.component';

// Thermostat Components
import { ThermostatsComponent } from './components/thermostats/thermostats.component';
import { ThermostatComponent } from './components/thermostat/thermostat.component';
import { TemperatureComponent } from './components/thermostat/components/temperature/temperature.component';
import { SettingsComponent } from './components/thermostat/components/settings/settings.component';
import { SensorComponent } from './components/thermostat/components/sensor/sensor.component';
import { WeatherChartComponent } from './components/thermostat/components/weather-chart/weather-chart.component';
import { OccupancyChartComponent } from './components/thermostat/components/occupancy-chart/occupancy-chart.component';
import { MessageComponent } from './components/thermostat/components/message/message.component';


import { AuthGuard } from './auth.guard';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: MainComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterUserComponent },
  { path: 'apps', component: AppsComponent, canActivate: [AuthGuard] },
  { path: 'apps/register', component: RegisterAppComponent, canActivate: [AuthGuard] },
  { path: 'thermostats', component: ThermostatsComponent, canActivate: [AuthGuard] },
  { path: 'thermostats/:key', component: ThermostatsComponent, canActivate: [AuthGuard] },
  { path: 'thermostats/:key/:identifier', component: ThermostatComponent, canActivate: [AuthGuard] },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }

export const RoutingComponents = [
  MainComponent,
  NavbarComponent,
  RegisterUserComponent,
  LoginComponent,
  AppsComponent,
  RegisterAppComponent,
  ThermostatsComponent,
  ThermostatComponent,
  TemperatureComponent,
  SettingsComponent,
  SensorComponent,
  WeatherChartComponent,
  OccupancyChartComponent,
  MessageComponent,
  PageNotFoundComponent,
]
