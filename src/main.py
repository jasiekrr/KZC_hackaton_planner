from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Annotated
import json
import os

ID_counter: int = 0

actFileName = "activities.txt"
subjFileName = "subjects.txt"
is_data_up_to_date = False  # when program begins data is not read from the files - it needs to read it in order to work

subjects = {
    "1": {"subjectName": "TGiS",
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
}

activities: dict = {}

class Activity:
    studentId: int
    subjectName: str
    mainTeacher: str
    format: str
    type: str
    deadline: str
    done: str
    Id: int



def read_data():
    global ID_counter
    global subjects
    global activities
    global is_data_up_to_date
    if os.path.exists(actFileName):
        with open(actFileName, "r") as f:
            all_activities = f.readlines()
            for act in all_activities:
                jsondict = eval(act)
                for key, value in jsondict.items():
                    if int(key) > ID_counter:
                        ID_counter = int(key)
                    activity = Activity()
                    activity.__dict__ = eval(jsondict[key]).copy()
                    activities[int(key)] = activity



    if  os.path.exists(subjFileName):
        with open(subjFileName, "r") as f:
            all_subjects = f.readlines()
            for sub in all_subjects:
                pass



if is_data_up_to_date is False:
    read_data()
    print("\n----------Data was read from the database, app is ready for work---------\n")
    is_data_up_to_date = True


app = FastAPI()


def write_data(what_to_write):
    """

    :param what_to_write: if it is "sub" it writes subjects to the "database". If it is "act" it does so for
    the activities. Every other value is ignored
    :return:
    """
    if what_to_write == "sub":
        with open(subjFileName, "w") as f:
            for key, val in subjects.items():
                f.write( str({str(key) : str(val.__dict__)}) + "\n")
    elif what_to_write == "act":
        with open(actFileName, "w") as f:
            for key, val in activities.items():
                print(key, val.__dict__)

                f.write(str({str(key): str(val.__dict__)}) + "\n")

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
    Id: int
    studentId: int
    subjectName: str
    mainTeacher: str
    format: str
    type: str
    deadline: str
    done: str








@app.post("/activities/")
def create_activity(activity: Annotated[ActivityRequest, Body()]):
    global ID_counter
    ID_counter += 1
    tempID = ID_counter
    subj = activity.subjectName
    newActivity = Activity()
    newActivity.__dict__ = activity.__dict__.copy()

    newActivity.done = "false"
    newActivity.Id = tempID
    activities[tempID] = newActivity
    write_data("act")
    return newActivity


@app.get("/activities/")
def read_activities():
    return list(activities.values())


@app.get("/activities/{index}")
def read_activities(index: int):
    print(activities)
    if index not in activities:
        return 404
    return activities[index]


@app.put("/activities/")
async def change_activity(activity: Annotated[ChangeActivityRequest, Body()]):
    changedID = activity.Id
    if changedID in activities:
        oldActivity = activities[changedID]
        oldActivity.__dict__ = activity.__dict__.copy()
        write_data("act")
        return activity

@app.delete("/activities/{index}", status_code=200)
def remove_act(index: int):
    if index not in activities:
        return 404
    del activities[index]
    write_data("act")



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
