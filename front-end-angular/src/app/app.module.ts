import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { AppRoutingModule, RoutingComponents } from './app-routing.module';
import { AuthGuard } from './auth.guard'
import { AppService } from './app.service';

@NgModule({
  declarations: [
    AppComponent,
    RoutingComponents,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [AppService, AuthGuard],
  bootstrap: [AppComponent]
})
export class AppModule { }
