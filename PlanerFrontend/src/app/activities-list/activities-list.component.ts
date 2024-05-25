// src/app/subject-list/subject-list.component.ts
import { Component, OnInit } from '@angular/core';
import { Activity } from '../models/activity';
import { ActiviesHttpService } from '../services/activities-http-service';
import {
  Observable,
  Subject,
  finalize,
  lastValueFrom,
  of,
  switchMap,
} from 'rxjs';

@Component({
  selector: 'app-activities-list',
  templateUrl: './activities-list.component.html',
  styleUrls: ['./activities-list.component.css'],
})
export class ActivitiesListComponent implements OnInit {
  displayedColumns: string[] = [
    'subjectName',
    'mainTeacher',
    'format',
    'type',
    'deadline',
    'done',
  ];
  progressSpinnerVisible: boolean = true;
  awaitingPlayersSpinnerVisible: boolean = false;

  activities: Activity[] = [];

  constructor(private activiesHttpService: ActiviesHttpService) {}

  async ngOnInit(): Promise<void> {
    const activities$ = this.activiesHttpService.getActivities();
    var activities = await lastValueFrom(this.loadData(activities$));

    this.activities = activities;
  }

  toggleDone(element: Activity): void {
    element.done = !element.done;
    this.updateActivityAsync(element);
  }

  private loadData(obs$: Observable<any>): Observable<any> {
    return of((this.progressSpinnerVisible = true)).pipe(
      switchMap(() => obs$),
      finalize(() => (this.progressSpinnerVisible = false))
    );
  }

  private async updateActivityAsync(activity: Activity){
    const activity$ = this.activiesHttpService.updateActivity(activity);
    var obtainedActivity = await lastValueFrom(this.loadData(activity$));

    const activities$ = this.activiesHttpService.getActivities();
    var activities = await lastValueFrom(this.loadData(activities$));

    this.activities = activities;
  }
}
