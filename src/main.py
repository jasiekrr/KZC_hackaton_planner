from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Annotated

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ID_counter: int = 0

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Subject(BaseModel):
    subjectName: str
    mainTeacher: str
    ects: int
    formats: List[dict]


class ActivityRequest(BaseModel):
    studentId: int
    subjectName: str
    mainTeacher: str
    format: str
    type: str
    deadline: str


class ChangeActivityRequest(BaseModel):
    id: int
    studentId: int
    subjectName: str
    mainTeacher: str
    format: str
    type: str
    deadline: str
    done: str


class Activity:
    studentId: int
    subjectName: str
    mainTeacher: str
    format: str
    type: str
    deadline: str
    done: str
    id: int


subjects = [
    {"subjectName": "TGiS",
     "mainTeacher": "Zbigniew Tarapata",
     "ects": 4,
     "formats": [
         {
             "formatType": "lecture",
             "numberOfHours": 30
         },
         {
             "formatType": "laboratory",
             "numberOfHours": 40
         }
     ]
     }
]

activities: dict = {}


@app.post("/activities/")
def create_activity(activity: Annotated[ActivityRequest, Body()]):
    global ID_counter
    ID_counter += 1
    tempID = ID_counter
    subj = activity.subjectName
    newActivity = Activity()
    newActivity.__dict__ = activity.__dict__.copy()

    newActivity.done = "false"
    newActivity.ID = tempID
    activities[tempID] = newActivity
    return newActivity


@app.get("/activities/")
def read_activities():
    return list(activities.values())


@app.get("/activities/{index}")
def read_activities(index: int):
    if index not in activities:
        return 404
    return activities[index]


@app.put("/activities/")
async def create_activity(activity: Annotated[ChangeActivityRequest, Body()]):
    subj = activity.subjectName
    changedID = activity.ID
    if changedID in activities:
        oldActivity = activities[changedID]
        oldActivity.__dict__ = activity.__dict__.copy()
        return activity

@app.delete("/activities/{index}", status_code=200)
def remove_act(index: int):
    if index not in activities:
        return 404
    del activities[index]



@app.get("/subjects/")
def read_subjects():
    answer_dict = {}
    answer_dict["semesterEnds"] = "2024-05-25T14:30:00Z"
    answer_dict["overallEcts"] = 30
    answer_dict["subjects"] = subjects
    return answer_dict


# @app.get("/nowy/")
# def sztuczny_create():
#     subjects.append({"subjectName": "UpdatedSubject", "mainTeacher": "Jane Smith", "ects": 6,
#                      "formats": [{"formatType": "seminar", "numberOfHours": 60},
#                                  {"formatType": "practical", "numberOfHours": 55}]})
#     return {"subjectName": "UpdatedSubject", "mainTeacher": "Jane Smith", "ects": 6,
#             "formats": [{"formatType": "seminar", "numberOfHours": 60},
#                         {"formatType": "practical", "numberOfHours": 55}]}


@app.get("/subjects/{index}")
def read_subject(index: int):
    return subjects[index - 1]


@app.post("/subjects/")
def create_subject(subject: Annotated[Subject, Body()]):
    subjects.append(subject.__dict__)
    return subject


@app.put("/subjects/{id}")
def update_subject(id: int, subject: Subject):
    for index, s in enumerate(subjects):
        if s["subjectName"] == id:
            subjects[index] = subject.dict()
            return subject
    raise HTTPException(status_code=404, detail="Subject not found")


@app.delete("/subjects/{id}")
async def delete_subject(id: int):
    global subjects
    subjects = [s for s in subjects if s["subjectName"] != id]
    return {"detail": f"Subject {id} deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
