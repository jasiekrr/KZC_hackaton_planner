# import datetime
# from pydantic import BaseModel
# from typing import List
#
# class Task(BaseModel):
#     name: str
#     deadline: datetime.datetime
#     duration: int  # Duration in minutes
#     studentID: int
#
# class TimeFrame(BaseModel):
#     start: datetime.datetime
#     end: datetime.datetime
#
# class TaskPlanner:
#     def __init__(self):
#         self.tasks = []
#         self.time_frames = []
#         self.planned_tasks = []
#
#     def add_task(self, task: Task):
#         self.tasks.append(task)
#
#     def add_time_frame(self, time_frame: TimeFrame):
#         self.time_frames.append(time_frame)
#
#     def plan_tasks(self):
#         self.tasks.sort(key=lambda task: task.deadline)
#         for task in self.tasks:
#             remaining_duration = datetime.timedelta(minutes=task.duration)
#             for time_frame in self.time_frames:
#                 while remaining_duration > datetime.timedelta(minutes=0):
#                     available_duration = time_frame.end - time_frame.start
#                     if available_duration <= datetime.timedelta(minutes=0):
#                         break
#                     task_start = max(datetime.datetime.now(), time_frame.start)
#                     if available_duration >= remaining_duration:
#                         task_end = task_start + remaining_duration
#                         if task_end <= task.deadline:
#                             self.planned_tasks.append({
#                                 "task": task.name,
#                                 "studentID": task.studentID,
#                                 "start": task_start,
#                                 "end": task_end
#                             })
#                             time_frame.start = task_end
#                             remaining_duration = datetime.timedelta(minutes=0)
#                         else:
#                             break
#                     else:
#                         task_end = task_start + available_duration
#                         self.planned_tasks.append({
#                             "task": task.name + " (part)",
#                             "studentID": task.studentID,
#                             "start": task_start,
#                             "end": task_end
#                         })
#                         time_frame.start = task_end
#                         remaining_duration -= available_duration
#
#     def list_all_tasks(self):
#         return self.tasks
#
#     def list_planned_tasks(self):
#         return self.planned_tasks
#
# # Create an instance of TaskPlanner
# planner = TaskPlanner()
#
# # Add initial data
# initial_tasks = [
#     Task(name="Task 1", deadline=datetime.datetime(2024, 6, 1, 10, 0), duration=120, studentID=1),
#     Task(name="Task 2", deadline=datetime.datetime(2024, 6, 1, 12, 0), duration=90, studentID=2),
#     Task(name="Task 3", deadline=datetime.datetime(2024, 6, 1, 9, 0), duration=60, studentID=1)
# ]
#
# initial_time_frames = [
#     TimeFrame(start=datetime.datetime(2024, 6, 1, 8, 0), end=datetime.datetime(2024, 6, 1, 10, 0)),
#     TimeFrame(start=datetime.datetime(2024, 6, 1, 10, 0), end=datetime.datetime(2024, 6, 1, 12, 0)),
#     TimeFrame(start=datetime.datetime(2024, 6, 1, 13, 0), end=datetime.datetime(2024, 6, 1, 15, 0))
# ]
#
# for task in initial_tasks:
#     planner.add_task(task)
#
# for time_frame in initial_time_frames:
#     planner.add_time_frame(time_frame)
#
#
#
# def main():
#     while True:
#         print("\nTask Planner")
#         print("1. Add Task")
#         print("2. Add Time Frame")
#         print("3. Plan Tasks")
#         print("4. List All Tasks")
#         print("5. List Planned Tasks")
#         print("6. Exit")
#
#         choice = input("Choose an option: ")
#
#         if choice == '1':
#             name = input("Task name: ")
#             deadline_str = input("Task deadline (YYYY-MM-DD HH:MM): ")
#             duration = int(input("Task duration (minutes): "))
#             studentID = int(input("Student ID: "))
#             deadline = datetime.datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
#             task = Task(name=name, deadline=deadline, duration=duration, studentID=studentID)
#             planner.add_task(task)
#             print("Task added successfully.")
#
#         elif choice == '2':
#             start_str = input("Time frame start (YYYY-MM-DD HH:MM): ")
#             end_str = input("Time frame end (YYYY-MM-DD HH:MM): ")
#             start = datetime.datetime.strptime(start_str, '%Y-%m-%d %H:%M')
#             end = datetime.datetime.strptime(end_str, '%Y-%m-%d %H:%M')
#             time_frame = TimeFrame(start=start, end=end)
#             planner.add_time_frame(time_frame)
#             print("Time frame added successfully.")
#
#         elif choice == '3':
#             planner.plan_tasks()
#             print("Tasks have been planned.")
#
#         elif choice == '4':
#             all_tasks = planner.list_all_tasks()
#             for task in all_tasks:
#                 print(f"Task Name: {task.name}, Deadline: {task.deadline}, Duration: {task.duration} minutes, Student ID: {task.studentID}")
#
#         elif choice == '5':
#             planned_tasks = planner.list_planned_tasks()
#             if planned_tasks:
#                 for task in planned_tasks:
#                     print(f"Task {task['task']} (Student ID: {task['studentID']}) scheduled from {task['start']} to {task['end']}")
#             else:
#                 print("No tasks have been planned yet.")
#
#         elif choice == '6':
#             print("Exiting...")
#             break
#
#         else:
#             print("Invalid choice. Please try again.")
#
#
#
#
# if __name__ == "__main__":
#     main()



from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import datetime


class Task(BaseModel):
    name: str
    deadline: datetime.datetime
    duration: int  # Duration in minutes
    studentID: int

class TimeFrame(BaseModel):
    start: datetime.datetime
    end: datetime.datetime

class TaskPlanner:
    def __init__(self):
        self.tasks = []
        self.time_frames = []
        self.planned_tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def add_time_frame(self, time_frame: TimeFrame):
        self.time_frames.append(time_frame)

    def plan_tasks(self):
        self.tasks.sort(key=lambda task: task.deadline)
        for task in self.tasks:
            remaining_duration = datetime.timedelta(minutes=task.duration)
            for time_frame in self.time_frames:
                while remaining_duration > datetime.timedelta(minutes=0):
                    available_duration = time_frame.end - time_frame.start
                    if available_duration <= datetime.timedelta(minutes=0):
                        break
                    task_start = max(datetime.datetime.now(), time_frame.start)
                    if available_duration >= remaining_duration:
                        task_end = task_start + remaining_duration
                        if task_end <= task.deadline:
                            self.planned_tasks.append({
                                "task": task.name,
                                "studentID": task.studentID,
                                "start": task_start,
                                "end": task_end
                            })
                            time_frame.start = task_end
                            remaining_duration = datetime.timedelta(minutes=0)
                        else:
                            break
                    else:
                        task_end = task_start + available_duration
                        self.planned_tasks.append({
                            "task": task.name + " (part)",
                            "studentID": task.studentID,
                            "start": task_start,
                            "end": task_end
                        })
                        time_frame.start = task_end
                        remaining_duration -= available_duration

    def list_all_tasks(self):
        return self.tasks

    def list_planned_tasks(self):
        return self.planned_tasks

# Singleton instance of TaskPlanner
task_planner = TaskPlanner()

# Dependency to get the TaskPlanner instance
def get_task_planner():
    return task_planner




class Task(BaseModel):
    taskID: int
    name: str
    deadline: datetime.datetime
    duration: int  # Duration in minutes
    studentID: int

class TimeFrame(BaseModel):
    start: datetime.datetime
    end: datetime.datetime

class TaskPlanner:
    def __init__(self):
        self.tasks = []
        self.time_frames = []
        self.planned_tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def add_time_frame(self, time_frame: TimeFrame):
        self.time_frames.append(time_frame)

    def plan_tasks(self):
        self.tasks.sort(key=lambda task: task.deadline)
        for task in self.tasks:
            remaining_duration = datetime.timedelta(minutes=task.duration)
            for time_frame in self.time_frames:
                while remaining_duration > datetime.timedelta(minutes=0):
                    available_duration = time_frame.end - time_frame.start
                    if available_duration <= datetime.timedelta(minutes=0):
                        break
                    task_start = max(datetime.datetime.now(), time_frame.start)
                    if available_duration >= remaining_duration:
                        task_end = task_start + remaining_duration
                        if task_end <= task.deadline:
                            self.planned_tasks.append({
                                "task": task.name,
                                "studentID": task.studentID,
                                "start": task_start,
                                "end": task_end
                            })
                            time_frame.start = task_end
                            remaining_duration = datetime.timedelta(minutes=0)
                        else:
                            break
                    else:
                        task_end = task_start + available_duration
                        self.planned_tasks.append({
                            "task": task.name + " (part)",
                            "studentID": task.studentID,
                            "start": task_start,
                            "end": task_end
                        })
                        time_frame.start = task_end
                        remaining_duration -= available_duration
        print(self.planned_tasks)

    def list_all_tasks(self):
        return self.tasks

    def list_planned_tasks(self):
        return self.planned_tasks

# Singleton instance of TaskPlanner
task_planner = TaskPlanner()

# Dependency to get the TaskPlanner instance
def get_task_planner():
    return task_planner

