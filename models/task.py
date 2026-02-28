import json, os
from utils.storage_handler import save_to_file, load_from_file


class Task:
    tasks = []
    task_data = "data/tasks.json"
    id_counter = 1

    def __init__(self, project_id, title, assigned_to, status="Incomplete", id=None):
        self.project_id = project_id
        self.title = title
        self.status = status
        self.assigned_to = assigned_to
        #if no id is provided.
        if id is None:
            #assign an id using the id counter which is 1 at the beginning.ensures each task has unique id.
            self.id = Task.id_counter
        else:
            self.id = id
        #if the id we assigned is greater than or equal to 1(the current value of th id counter)
        if self.id >= Task.id_counter:
            #increment the id counter to be one more,ensures we don't reuse the same id.
            Task.id_counter = self.id + 1

        Task.tasks.append(self)
        
    def mark_as_complete(self):
        self.status = "Complete"
        

    @classmethod
    def read_from_file(cls):
        #check if the tasks json file exists
        if not os.path.exists(cls.task_data):
            #if it does'nt exist ,create an empty list of tasks.
            cls.tasks = []
            cls.id_counter = 1
            return
        try:
            data = load_from_file(cls.task_data)
            cls.tasks = []
            cls.id_counter = 1
            if data is None:
                print(f"No tasks found in the tasks")
            for task in data:
                #create the task object for every task, cls(...) triggers the __init__  method 
                # and adds the task  to cls.task automatically
                 cls(
                    id=task.get("id"),
                    project_id=task.get("project_id"),
                    title=task.get("title"),
                    status=task.get("status"),
                    assigned_to=task.get("assigned_to"),
                 )
        except Exception as e:
            print(f"Error loading file: {e}")

    @classmethod
    def save_to_file(cls):
        try:
            save_to_file(cls.tasks, cls.task_data)
            print(f"Tasks saved to: {cls.task_data}")
        except PermissionError:
            print(f"Error: Permission denied when writing to {cls.task_data}")
        except OSError as e:
            # for errors like disk full
            print(f"❌ System Error: {e}")
        except Exception as e:
            # for any other unexpected bugs
            print(f"❌ An unexpected error occurred: {e}")

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "assigned_to": self.assigned_to,
            "status": self.status,
        }
