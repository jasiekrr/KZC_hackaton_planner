export interface Activity{
    ID: number;
    subjectName: string;
    mainTeacher: string;
    format: string;
    type: string;
    deadline: Date;
    done: boolean;
}