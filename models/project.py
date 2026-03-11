import json
from datetime import datetime
from utils.storage_handler import save_to_file, load_from_file

class Project:
    projects = []
    projects_data = "data/projects.json"
    id_counter = 1
    
    def __init__(self, title, description, due_date, owner_email, id=None):
        self.title = title
        self.description = description
        self.owner_email = owner_email
        # use the property setter to validate/normalize the due date
        self.due_date = due_date
        
        #if no id is provided, assign one using the class-level id counter. 
        # This ensures that each project has a unique id, even if some projects are deleted in the future.
        if id is None:
            self.id = Project.id_counter
        
        else:
            self.id = id
            
        # Update the id counter if the provided id is greater than or equal to the current counter value. 
        # This ensures that we don't accidentally reuse an id in the future.
        if self.id  >= Project.id_counter:
            Project.id_counter = self.id + 1
                 
        Project.projects.append(self)
    
    @property
    def due_date(self):
        return self._due_date
    
    #setter to validate date format.
    #TBD is a default value (to be determined) it sets a default date if the provided date is invalid, 
    # allowing the project to be created without a valid due date.
    @due_date.setter
    def due_date(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            self._due_date = value
        except ValueError:
            print("Due date must be in YYYY-MM-DD format")
            self._due_date = "TBD"
    
    #gets data from json file and creates project instances    
    @classmethod
    def read_from_file(cls):
        data = load_from_file(cls.projects_data)
        cls.projects = []
        #reste id counter to 1 when we read from file to avoid id conflicts when creating new projects.
        Project.id_counter = 1
            
        if data is None:
            return
        
        for project in data:
             cls(
                id = project.get('id'),
                title = project.get('title'), 
                description = project.get('description'), 
                due_date = project.get('due_date', "TBD"), 
                owner_email = project.get('owner_email')
            )
            
            
    #saves project instances to json file
    @classmethod
    def save_projects_to_file(cls):
        try:
            save_to_file(cls.projects, cls.projects_data)
        except Exception as e:
            print(f"An error occurred while saving projects: {e}")
        
    #converts project instance to a dictionary for better readability in the JSON file.
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner_email": self.owner_email
        }

    @classmethod
    def delete_project(cls, project_id):
    
        project_to_delete =  next((project for project in cls.projects if project.id == project_id), None)
        if project_to_delete:
            cls.projects.remove(project_to_delete)
            cls.save_projects_to_file()
            return True
        return False    
        