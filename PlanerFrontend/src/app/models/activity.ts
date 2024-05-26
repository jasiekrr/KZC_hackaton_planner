export interface Activity{
    Id: number;
    subjectName: string;
    mainTeacher: string;
    format: string;
    type: string;
    deadline: Date;
    done: boolean;
}

export interface UpdateActivityRequest{
    Id: number;
    studentId: number;
    subjectName: string;
    mainTeacher: string;
    format: string;
    type: string;
    deadline: string;
    done: string;
}

export interface CreateActivityRequest{
    studentId: number;
    subjectName: string;
    mainTeacher: string;
    format: string;
    type: string;
    deadline: string;
    done: string;
}

export interface CreateActivityResponse{
    Id: number,
    studentId: number;
    subjectName: string;
    mainTeacher: string;
    format: string;
    type: string;
    deadline: string;
    done: string;
}