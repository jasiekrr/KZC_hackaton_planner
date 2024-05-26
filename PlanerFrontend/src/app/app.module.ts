import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { MatTableModule } from '@angular/material/table';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatCardModule } from '@angular/material/card';

import { AppComponent } from './app.component';
import { ActivitiesListComponent } from './activities-list/activities-list.component';
import { AppRoutingModule } from './app-routing.module';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { HttpClientModule } from '@angular/common/http';
import { AddActivityDialogComponent } from './add-activity-dialog/add-activity-dialog.component';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { MatNativeDateModule } from '@angular/material/core';
import { MatAutocompleteModule } from '@angular/material/autocomplete';

@NgModule({
  declarations: [
    AppComponent,
    ActivitiesListComponent,
    AddActivityDialogComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    MatTableModule,
    ProgressSpinnerModule,
    MatCheckboxModule,
    MatAutocompleteModule,
    MatCardModule,
    HttpClientModule,
    MatFormFieldModule,
    MatSelectModule,
    FormsModule,
    ReactiveFormsModule,
    MatNativeDateModule,
    MatButtonModule,
    MatDialogModule,
    MatInputModule,
    MatDatepickerModule,
    RouterModule.forRoot([
      { path: 'activities', component: ActivitiesListComponent },
    ]),
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
