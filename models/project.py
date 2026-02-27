class Project:
    projects = []
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        
        Project.projects.append(self)
        
    #for clean output    
    def __str__(self):
        return f"Project: '{self.title}', | Description: '{self.description}', | Due Date: '{self.due_date}'"