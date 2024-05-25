// src/app/subject-list/subject-list.component.ts
import { Component, OnInit } from '@angular/core';
import { Activity } from '../models/activity.ts';
import { ActiviesHttpService } from '../services/activities-http-service.ts';
import { Observable, finalize, lastValueFrom, of, switchMap } from 'rxjs';

@Component({
  selector: 'app-activities-list',
  templateUrl: './activities-list.component.html',
  styleUrls: ['./activities-list.component.css']
})
export class ActivitiesListComponent implements OnInit {

  displayedColumns: string[] = ['subjectName', 'mainTeacher', 'format', 'type', 'deadline', 'done'];
  progressSpinnerVisible: boolean = true;
  awaitingPlayersSpinnerVisible: boolean = false;

  activities: Activity[] = [
    {
      id: 1,
      subjectName: 'TGiS',
      mainTeacher: 'Zbigniew Tarapata',
      format: 'lecture',
      type: 'project',
      deadline: new Date('2024-05-25T14:30:00Z'),
      done: 'true'
    },
    // Dodaj tutaj więcej elementów, jeśli potrzebujesz
  ];

  constructor(private activiesHttpService: ActiviesHttpService) { }

  async ngOnInit(): Promise<void> {
    const activities$ = this.activiesHttpService.getActivities();
    var activities = await lastValueFrom(this.loadData(activities$))
   }

   private loadData(obs$: Observable<any>): Observable<any> {
    return of((this.progressSpinnerVisible = true)).pipe(
      switchMap(() => obs$),
      finalize(() => (this.progressSpinnerVisible = false))
    );
  }
}
