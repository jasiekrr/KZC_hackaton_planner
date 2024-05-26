import datetime

from fastapi import Body
from pydantic import BaseModel
from typing import List, Annotated
import os

from fastapi import FastAPI, HTTPException, Depends
from typing import List

from src.planer import Task, TaskPlanner, TimeFrame, get_task_planner

ID_counter: int = 0
task_ID_counter: int = 0
actFileName = "activities.txt"
subjFileName = "subjects.txt"
taskFilename = "tasks.txt"
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

przedmiotyWybieralne = ["TGiS", "WdA", "TIiK", "MD1", "MD2", "MM", "M1", "M2", "AM", "WDI", "WDP", "PO", "PW", "OWI"]
prowadzacyWybieralni = ["Zbigniew Tarapata", "Wlodzimierz Kwiatkowski", "Andrzej Chojnacki", "Arkadiusz Szymaniec",
                        "Dariusz Pierzchala", "Tadeusz Nowicki", "Radoslaw Rulka", "Typ od OWI"]
rygoryWybieralne = ["Zaliczenie", "Egzamin", "Kolokwium", "DOWALONE KOLOKWIUM", "sprawozdanie", "projekt",
                    "projekt semestralny", "ciezkie sprawozdanie"]

przedmiotyWybieralne.sort()
prowadzacyWybieralni.sort()
rygoryWybieralne.sort()

activities: dict = {}

slownikiTaskow = {}

class Activity:
    studentId: int
    subjectName: str
    mainTeacher: str
    format: str
    type: str
    deadline: str
    done: str
    Id: int


pureActivities = [{"studentID" : 1, "subjectName": "WdA", "mainTeacher": "Wlodzimierz Kwiatkowski",
                  "format": "wyklad", "type": "kolokwium", "timeNeeded": 120, "deadline": datetime.datetime(2024,5,30),
                   "done": "false", "Id": 1},
                  {"studentID": 1, "subjectName": "TIiK", "mainTeacher": "Wlodzimierz Kwiatkowski",
                   "format": "cwiczenia", "type": "cwiczenia", "timeNeeded": 90, "deadline": datetime.datetime(2024, 5, 28),
                   "done": "false", "Id": 1},
    {"studentID": 1, "subjectName": "TIiK", "mainTeacher": "Wlodzimierz Kwiatkowski", "format": "cwiczenia", "type": "cwiczenia", "timeNeeded": 90, "deadline": "2024-05-28T00:00:00", "done": "false", "Id": 1},
    {"studentID": 1, "subjectName": "M2", "mainTeacher": "Arkadiusz Szymaniec", "format": "wyklad", "type": "wyklad", "timeNeeded": 60, "deadline": "2024-06-01T00:00:00", "done": "false", "Id": 2},
    {"studentID": 1, "subjectName": "FI", "mainTeacher": "Jan Kowalski", "format": "lab", "type": "lab", "timeNeeded": 120, "deadline": "2024-06-05T00:00:00", "done": "false", "Id": 3},
    {"studentID": 1, "subjectName": "PO", "mainTeacher": "Tadeusz Nowicki", "format": "wyklad", "type": "wyklad", "timeNeeded": 90, "deadline": "2024-06-08T00:00:00", "done": "true", "Id": 4},
    {"studentID": 1, "subjectName": "MD2", "mainTeacher": "Andrzej Chojnacki", "format": "seminar", "type": "seminarium", "timeNeeded": 75, "deadline": "2024-06-10T00:00:00", "done": "false", "Id": 5},
    {"studentID": 1, "subjectName": "MM", "mainTeacher": "Andrzej Chojnacki", "format": "lecture", "type": "wykład", "timeNeeded": 45, "deadline": "2024-06-15T00:00:00", "done": "true", "Id": 6},
    {"studentID": 1, "subjectName": "MD1", "mainTeacher": "Arkadiusz Szymaniec", "format": "cwiczenia", "type": "praca dom", "timeNeeded": 120, "deadline": "2024-06-25T00:00:00", "done": "false", "Id": 8},
    {"studentID": 1, "subjectName": "AM", "mainTeacher": "Arkadziusz Szymaniec", "format": "cwiczenia", "type": "prezentacja", "timeNeeded": 90, "deadline": "2024-06-30T00:00:00", "done": "true", "Id": 9},
    {"studentID": 1, "subjectName": "WF", "mainTeacher": "Michal Gąsiński", "format": "cwiczenia", "type": "bieganie po lesie", "timeNeeded": 60, "deadline": "2024-07-05T00:00:00", "done": "false", "Id": 10},
    {"studentID": 1, "subjectName": "WdA", "mainTeacher": "Włodzimierz Kwiatkowski", "format": "project", "type": "projekt", "timeNeeded": 150, "deadline": "2024-07-10T00:00:00", "done": "false", "Id": 11}
]

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
    else:
        for wpis in pureActivities:
            temp = Activity()
            temp.__dict__ = wpis
            activities[temp.Id] = temp

    if os.path.exists(subjFileName):
        with open(subjFileName, "r") as f:
            all_subjects = f.readlines()
            for sub in all_subjects:
                pass


if is_data_up_to_date is False:
    read_data()
    print("\n----------Data was read from the database, app is ready for work---------\n")
    is_data_up_to_date = True

app = FastAPI()


@app.get("/choices/prow/")
def get_prowadzacy():
    return prowadzacyWybieralni


@app.get("/choices/przed/")
def get_przedmioten():
    return przedmiotyWybieralne


@app.get("/choices/rygory")
def get_rygoren():
    return rygoryWybieralne


def write_data(what_to_write):
    """

    :param what_to_write: if it is "sub" it writes subjects to the "database". If it is "act" it does so for
    the activities. Every other value is ignored
    :return:
    """
    if what_to_write == "sub":
        with open(subjFileName, "w") as f:
            for key, val in subjects.items():
                f.write(str({str(key): str(val.__dict__)}) + "\n")
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
    timeNeeded: int
    deadline: str


class ChangeActivityRequest(BaseModel):
    Id: int
    studentId: int
    subjectName: str
    mainTeacher: str
    format: str
    type: str
    timeNeeded: int
    deadline: str
    done: str


@app.post("/activities/")
def create_activity(activity: Annotated[ActivityRequest, Body()]):
    global ID_counter
    ID_counter += 1
    tempID = ID_counter
    newActivity = Activity()
    newActivity.__dict__ = activity.__dict__.copy()

    newActivity.done = "false"
    newActivity.Id = tempID
    activities[tempID] = newActivity
    write_data("act")
    return newActivity


    # studentId: int
    # subjectName: str
    # mainTeacher: str
    # format: str
    # type: str
    # deadline: str
    # done: str
    # Id: int







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
def update_subject(Id: int, subject: Subject):
    for index, s in enumerate(subjects):
        if s["subjectName"] == Id:
            subjects[index] = subject.dict()
            return subject
    raise HTTPException(status_code=404, detail="Subject not found")


@app.delete("/subjects/{id}")
async def delete_subject(Id: int):
    global subjects
    subjects = [s for s in subjects if s["subjectName"] != Id]
    return {"detail": f"Subject {Id} deleted"}




# @app.post("/tasks/")
# async def create_task(task: Task, task_planner: TaskPlanner = Depends(get_task_planner)):
#     global task_ID_counter
#     task_ID_counter += 1
#
#     print("Wchodzi w create task")
#     task_planner.add_task(task)
#     return {"message": "Task added successfully."}
#
# @app.post("/timeframes/")
# async def create_time_frame(time_frame: TimeFrame, task_planner: TaskPlanner = Depends(get_task_planner)):
#     task_planner.add_time_frame(time_frame)
#     return {"message": "Time frame added successfully."}
#
# @app.post("/plan/")
# async def plan_tasks(task_planner: TaskPlanner = Depends(get_task_planner)):
#     task_planner.plan_tasks()
#     return {"message": "Tasks have been planned."}
#
# @app.get("/tasks/")
# async def read_all_tasks(task_planner: TaskPlanner = Depends(get_task_planner)):
#     all_tasks = task_planner.list_all_tasks()
#     return all_tasks
#
# @app.get("/planned_tasks/")
# async def read_planned_tasks(task_planner: TaskPlanner = Depends(get_task_planner)):
#     planned_tasks = task_planner.list_planned_tasks()
#     return planned_tasks
#


@app.post("/tasks/")
async def create_task(task: Task, task_planner: TaskPlanner = Depends(get_task_planner)):
    global task_ID_counter
    task_ID_counter+= 1
    task.taskID = task_ID_counter
    task_planner.add_task(task)
    return {"message": "Task added successfully."}

@app.post("/timeframes/")
async def create_time_frame(time_frame: TimeFrame, task_planner: TaskPlanner = Depends(get_task_planner)):
    task_planner.add_time_frame(time_frame)
    return {"message": "Time frame added successfully."}

@app.post("/plan/")
async def plan_tasks(task_planner: TaskPlanner = Depends(get_task_planner)):
    task_planner.plan_tasks()
    return {"message": "Tasks have been planned."}

@app.get("/tasks/")
async def read_all_tasks(task_planner: TaskPlanner = Depends(get_task_planner)):
    all_tasks = task_planner.list_all_tasks()
    return all_tasks

@app.get("/planned_tasks/")
async def read_planned_tasks(task_planner: TaskPlanner = Depends(get_task_planner)):
    planned_tasks = task_planner.list_planned_tasks()
    print(3*"\n", planned_tasks, 3*'\n')
    return planned_tasks



















if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
