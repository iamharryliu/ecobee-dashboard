import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { AppRoutingModule, RoutingComponents  } from './app-routing.module';

import { APIService } from './api.service';

@NgModule({
  declarations: [
    AppComponent,
    RoutingComponents,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [APIService],
  bootstrap: [AppComponent]
})
export class AppModule { }
