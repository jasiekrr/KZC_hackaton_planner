import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { MatTableModule } from '@angular/material/table';

import { AppComponent } from './app.component';
import { ActivitiesListComponent } from './activities-list/activities-list.component';
import { AppRoutingModule } from './app-routing.module';
import { ProgressSpinnerModule } from 'primeng/progressspinner';

@NgModule({
  declarations: [
    AppComponent,
    ActivitiesListComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatTableModule,
    ProgressSpinnerModule,
    RouterModule.forRoot([
      { path: 'activities', component: ActivitiesListComponent},
    ])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
