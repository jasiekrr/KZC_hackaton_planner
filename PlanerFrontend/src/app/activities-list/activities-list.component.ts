// src/app/subject-list/subject-list.component.ts
import { Component, OnInit } from '@angular/core';
import { Activity, UpdateActivityRequest } from '../models/activity';
import { ActiviesHttpService } from '../services/activities-http-service';
import {
  Observable,
  Subject,
  finalize,
  lastValueFrom,
  of,
  switchMap,
} from 'rxjs';
import { AddActivityDialogComponent } from '../add-activity-dialog/add-activity-dialog.component';
import { MatDialog } from '@angular/material/dialog';

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
  subjects: string[] = [];
  teachers: string[] = [];
  formats: string[] = [];
  types: string[] = [];

  constructor(
    private activiesHttpService: ActiviesHttpService,
    public dialog: MatDialog
  ) {}

  async ngOnInit(): Promise<void> {
    const activities$ = this.activiesHttpService.getActivities();
    var activities = await lastValueFrom(this.loadData(activities$));

    this.activities = activities;
    this.updateDropdownCollections();
  }

  toggleDone(element: Activity): void {
    element.done = !!element.done;
    element.done = !!element.done;
    this.updateActivityAsync(element);
  }

  openAddActivityDialog(): void {
    const dialogRef = this.dialog.open(AddActivityDialogComponent, {
      width: '400px',
      data: {
        subjects: this.subjects,
        teachers: this.teachers,
        formats: this.formats,
        types: this.types,
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.activities.push({
          ...result,
          id: this.activities.length + 1,
        });
      }
    });
  }

  private loadData(obs$: Observable<any>): Observable<any> {
    return of((this.progressSpinnerVisible = true)).pipe(
      switchMap(() => obs$),
      finalize(() => (this.progressSpinnerVisible = false))
    );
  }

  private async updateActivityAsync(activity: Activity) {
    const updateActivityRequest: UpdateActivityRequest = {
      Id: activity.Id,
      studentId: 1,
      subjectName: activity.subjectName,
      mainTeacher: activity.mainTeacher,
      format: activity.format,
      type: activity.type,
      deadline: activity.deadline.toString(),
      done: String(activity.done),
    };

    const activity$ = this.activiesHttpService.updateActivity(
      updateActivityRequest
    );
  }

  private updateDropdownCollections() {
    const uniqueSubjects = [
      ...new Set(this.activities.map((activity) => activity.subjectName)),
    ];

    this.subjects = uniqueSubjects;

    const uniqueTeachers = [
      ...new Set(this.activities.map((activity) => activity.mainTeacher)),
    ];

    this.teachers = uniqueTeachers;

    const uniqueFormats = [
      ...new Set(this.activities.map((activity) => activity.format)),
    ];

    this.formats = uniqueFormats;

    const uniqueTypes = [
      ...new Set(this.activities.map((activity) => activity.type)),
    ];

    this.types = uniqueTypes;
  }
}
