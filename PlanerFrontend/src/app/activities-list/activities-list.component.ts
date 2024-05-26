// src/app/subject-list/subject-list.component.ts
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Activity, CreateActivityRequest, UpdateActivityRequest } from '../models/activity';
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
    'actions'
  ];
  progressSpinnerVisible: boolean = true;
  awaitingPlayersSpinnerVisible: boolean = false;

  progressBarValue = 0;

  activities: Activity[] = [];
  subjects: string[] = [];
  teachers: string[] = [];
  formats: string[] = [];
  types: string[] = [];

  constructor(
    private activiesHttpService: ActiviesHttpService,
    public dialog: MatDialog,
    private cdRef: ChangeDetectorRef
  ) {}

  async ngOnInit(): Promise<void> {
    const activities$ = this.activiesHttpService.getActivities();
    var activities = await lastValueFrom(this.loadData(activities$));

    this.activities = activities;

    this.getPredefinedEnums();
    this.updateDropdownCollections();
    this.updateProgressBar()
  }

  toggleDone(element: Activity): void {
    element.done = (element.done.toString() == "true");
    element.done = !element.done
    this.updateActivityAsync(element);
    this.updateProgressBar();
  }

  openAddActivityDialog(): void {
    const dialogRef = this.dialog.open(AddActivityDialogComponent, {
      width: '600px', // Szerokość okna dialogowego
      height: '1000x', // Wysokość okna dialogowego
      data: {
        subjects: this.subjects,
        teachers: this.teachers,
        formats: this.formats,
        types: this.types,
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result && result.multiplier > 0) {
        const activityData = { ...result, done: false };
        const count = result.multiplier;
  
        Array.from({ length: count }).forEach(async () => {
          await this.createActivityAsync(activityData);
        });
      }
    });
  }

  async removeActivity(element: Activity){
    await this.activiesHttpService.deleteActivity(element.Id).toPromise();

    const activities$ = this.activiesHttpService.getActivities();
    var activities = await lastValueFrom(this.loadData(activities$));

    this.activities = activities;

    this.getPredefinedEnums();
    this.updateDropdownCollections();
    this.updateProgressBar()
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

    var activityValue = await lastValueFrom(this.loadData(activity$));
  }

  private async createActivityAsync(activity: Activity) {
    const createActivityRequest: CreateActivityRequest = {
      studentId: 1,
      subjectName: activity.subjectName,
      mainTeacher: activity.mainTeacher,
      format: activity.format,
      type: activity.type,
      deadline: activity.deadline.toString(),
      done: String(activity.done),
    };

    const activity$ = this.activiesHttpService.createActivity(
      createActivityRequest
    );

    var activities = await lastValueFrom(this.loadData(activity$));

    const activities$ = this.activiesHttpService.getActivities();
    var activities = await lastValueFrom(this.loadData(activities$));

    this.activities = activities;

    this.getPredefinedEnums();
    this.updateDropdownCollections();
  }

  private updateDropdownCollections() {
    const uniqueSubjects = [
      ...new Set(this.activities.map((activity) => activity.subjectName)),
    ];

    this.subjects = [ ...this.subjects, ...uniqueSubjects];
    this.subjects = [...new Set(this.subjects)]

    const uniqueTeachers = [
      ...new Set(this.activities.map((activity) => activity.mainTeacher)),
    ];

    this.teachers = [ ...this.teachers, ...uniqueTeachers];
    this.teachers = [...new Set(this.teachers)]

    const uniqueFormats = [
      ...new Set(this.activities.map((activity) => activity.format)),
    ];

    this.formats = [ ...this.formats, ...uniqueFormats];
    this.formats = [...new Set(this.formats)]

    const uniqueTypes = [
      ...new Set(this.activities.map((activity) => activity.type)),
    ];

    this.types = uniqueTypes;
  }

  private async getPredefinedEnums() {
    const subjects$ = this.activiesHttpService.getSubjects();
    var subjects = await lastValueFrom(this.loadData(subjects$));
    this.subjects = subjects;

    const teachers$ = this.activiesHttpService.getTeachers();
    var teachers = await lastValueFrom(this.loadData(teachers$));
    this.teachers = teachers;

    const formats$ = this.activiesHttpService.getFormats();
    var formats = await lastValueFrom(this.loadData(formats$));
    this.formats = formats;
  }

  private updateProgressBar(){
    const overall = this.activities.length
    const done = this.activities.filter(x => x.done == true || x.done.toString() == "true").length
    this.progressBarValue = done / overall * 100

    this.cdRef.detectChanges();
  }
}
