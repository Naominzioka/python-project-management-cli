from models.user import User
from models.project import Project
from models.task import Task
from tabulate import tabulate


    
#handler methods
def handle_add_user(args):
    #adding new user
    User(name=args.name, email=args.email)
    User.save_users_to_file()
    print(f"User {args.name} created")

def list_users(args):
    if not User.users:
        print("No users found.")
        return
    
    print("\n--- Current Users ---")
    table_data = []
    for person in User.users:
        table_data.append([person.name, person.email])
    print(tabulate(table_data, headers=["Name", "Email"], tablefmt="grid"))
    
def handle_add_project(args):
    user_exists = False
    for user in User.users:
        if user.email == args.owner_email:
            user_exists = True
            break # if we find a user with the matching email, we can stop searching through the list of users.
    if not user_exists:
        print(f"Error: No user with email {args.owner_email} found.")
        return
    
    Project(title=args.title, description=args.description, due_date=args.due_date, owner_email=args.owner_email)
    Project.save_projects_to_file()
    print(f"Project '{args.title}' created")
    
def handle_list_projects(args):
    user_projects = [project for project in Project.projects if project.owner_email == args.user]
    if not user_projects:
        print(f"No projects found for user with email {args.user}.")
        return
    
    print(f"\n--- Projects for {args.user} ---")
    table_data = []
    for project in user_projects:
        table_data.append([project.id, project.title, project.description, project.due_date])
    print(tabulate(table_data, headers=["ID", "Title", "Description", "Due Date"], tablefmt="grid"))
    
def handle_delete_project(args):
    project_to_delete = None
    for project in Project.projects:
        if project.id == args.project_id:
            project_to_delete = project
            break  #if we find the project, we can stop searching through the list of projects.
    
    if not project_to_delete:
        print(f"Error: No project with ID {args.project_id} found.")
        return
    
    Project.projects.remove(project_to_delete)
    Project.save_projects_to_file()
    print(f"Project with ID {args.project_id} deleted successfully.")
    
def handle_add_task(args):
    
    find_project = False
    for project in Project.projects:
        if project.id == args.project_id:
            find_project = True
            break # if we find a project with the matching id, we can stop searching through the list of projects.
    if not find_project:
        print(f"Error: Project with ID {args.project_id} not found.")
        return
    
    find_user = False
    for user in User.users:
        if user.email == args.assigned_to:
            find_user = True
            break # if we find a user with the matching email, we can stop searching through the list of users.
    if not find_user:
        print(f"Error: User with email {args.assigned_to} not found.")
        return
    Task(project_id=args.project_id, title=args.title, status=args.status, assigned_to=args.assigned_to)
    Task.save_to_file()
    print(f"✅ Task '{args.title}' added to Project {args.project_id}.")
    

def handle_completed_task(args):
    task_to_complete = None
    for task in Task.tasks:
        if task.id == args.task_id:
            task_to_complete = task
            break  #if we find the task, we can stop searching through the list of tasks.
    
    if not task_to_complete:
        print(f"❌ Error: No task found with ID {args.task_id}")
        return
    
    task_to_complete.mark_as_complete()
    print(f"✅ Task {args.task_id} ('{task_to_complete.title}') marked as Complete!")
    Task.save_to_file()