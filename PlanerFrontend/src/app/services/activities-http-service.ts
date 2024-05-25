import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Activity, UpdateActivityRequest } from "../models/activity";
import { Observable } from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class ActiviesHttpService {

    private readonly getActivitiesUrl = "http://localhost:8000/activities";

    activities: Activity[] = [
        {
          Id: 1,
          subjectName: 'TGiS',
          mainTeacher: 'Zbigniew Tarapata',
          format: 'lecture',
          type: 'project',
          deadline: new Date('2024-05-25T14:30:00Z'),
          done: true
        },
        // Dodaj tutaj więcej elementów, jeśli potrzebujesz
      ];
    

    constructor(private httpClient: HttpClient){

    }

    public getActivities(): Observable<Activity[]> {
        var reqHeader = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        return this.httpClient
            .get<Activity[]>(this.getActivitiesUrl, { headers: reqHeader });
    }

    public updateActivity(activity: UpdateActivityRequest): Observable<Activity> {
        var reqHeader = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        return this.httpClient
            .put<Activity>(this.getActivitiesUrl, activity, { headers: reqHeader });
    }
}