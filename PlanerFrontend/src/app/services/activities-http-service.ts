import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Activity, CreateActivityRequest, CreateActivityResponse, UpdateActivityRequest } from "../models/activity";
import { Observable } from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class ActiviesHttpService {

    private readonly getActivitiesUrl = "http://localhost:8000/activities";

    private readonly getSubjectsUrl = "http://localhost:8000/choices/przed";

    private readonly getTeachersUrl = "http://localhost:8000/choices/prow";

    private readonly getFormatsUrl = "http://localhost:8000/choices/rygory";

    activities: Activity[] = [ ];    

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

    public createActivity(activity: CreateActivityRequest): Observable<CreateActivityResponse> {
        var reqHeader = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        return this.httpClient
            .post<CreateActivityResponse>(this.getActivitiesUrl, activity, { headers: reqHeader });
    }

    public deleteActivity(activityId: number){
        var reqHeader = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        return this.httpClient
            .delete(this.getActivitiesUrl+'/'+activityId, { headers: reqHeader });
    }

    public getSubjects(): Observable<string[]> {
        var reqHeader = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        return this.httpClient
            .get<string[]>(this.getSubjectsUrl, { headers: reqHeader });
    }

    public getTeachers(): Observable<string[]> {
        var reqHeader = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        return this.httpClient
            .get<string[]>(this.getTeachersUrl, { headers: reqHeader });
    }

    public getFormats(): Observable<string[]> {
        var reqHeader = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        return this.httpClient
            .get<string[]>(this.getFormatsUrl, { headers: reqHeader });
    }
}