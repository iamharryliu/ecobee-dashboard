import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { AppRoutingModule, RoutingComponents  } from './app-routing.module';
import { HttpClientModule } from '@angular/common/http';

import { APIService } from './api.service';
import { TemperatureComponent } from './components/thermostat/components/temperature/temperature.component';
import { SettingsComponent } from './components/thermostat/components/settings/settings.component';
import { SensorsComponent } from './components/thermostat/components/sensors/sensors.component';
@NgModule({
  declarations: [
    AppComponent,
    RoutingComponents,
    TemperatureComponent,
    SettingsComponent,
    SensorsComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [APIService],
  bootstrap: [AppComponent]
})
export class AppModule { }
