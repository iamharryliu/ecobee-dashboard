import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { NavbarComponent } from './components/layout/navbar/navbar.component';
import { MainComponent } from './components/main/main.component';

import { AppsComponent } from './components/apps/apps.component'
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { RegisterAppComponent } from './components/register-app/register-app.component';
import { AppFormComponent } from './components/register-app/components/app-form/app-form.component';

import { ThermostatsComponent } from './components/thermostats/thermostats.component'
import { ThermostatComponent } from './components/thermostat/thermostat.component';
import { TemperatureComponent } from './components/thermostat/components/temperature/temperature.component';
import { SettingsComponent } from './components/thermostat/components/settings/settings.component';
import { SensorComponent } from './components/thermostat/components/sensor/sensor.component';
import { MessageComponent } from './components/thermostat/components/message/message.component';

const routes: Routes = [

    {path: '', component: MainComponent},

    {path: 'login', component: LoginComponent},
    {path: 'register', component: RegisterComponent},

    {path: 'register_app', component: RegisterAppComponent},
    {path: 'apps', component: AppsComponent},

    {path: 'apps/:key', component: ThermostatsComponent},
    {path: 'apps/:key/:identifier', component: ThermostatComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
export const RoutingComponents = [MainComponent,
                                NavbarComponent,
                                AppsComponent,
                                LoginComponent,
                                RegisterComponent,
                                RegisterAppComponent,
                                AppFormComponent,
                                ThermostatsComponent,
                                ThermostatComponent,
                                TemperatureComponent,
                                SettingsComponent,
                                SensorComponent,
                                MessageComponent,]
