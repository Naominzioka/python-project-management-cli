from models.user import User
from models.project import Project
from models.task import Task
import argparse
from tabulate import tabulate

class CLI:
    def __init__(self):
        #load existing data
        User.read_from_file()
        Project.read_from_file()
        Task.read_from_file()
        
        self.parser = argparse.ArgumentParser(description="Project Manager CLI")
        subparsers = self.parser.add_subparsers(dest="command")
        
        #add user    
        user_parser = subparsers.add_parser("add-user")
        user_parser.add_argument('name', help="Name of user")
        user_parser.add_argument('email', help="Email address of user")
        user_parser.set_defaults(func=self.handle_add_user)
        
        #list users
        list_users_parser = subparsers.add_parser("list-users")
        list_users_parser.set_defaults(func=self.list_users)
        
        #add project
        project_parser = subparsers.add_parser("add-project")
        project_parser.add_argument('title', help="Name of project")
        project_parser.add_argument('description', help="Description of project")
        project_parser.add_argument('due_date', help="Due date of project -Format: YYYY-MM-DD")
        project_parser.add_argument('owner_email', help="Email of the project owner")
        project_parser.set_defaults(func=self.handle_add_project)
        
        #list projects
        list_project_parser = subparsers.add_parser("list-projects")
        list_project_parser.add_argument('user', help="Email of the user associated with a certain project")
        list_project_parser.set_defaults(func=self.handle_list_projects)
        
        #delete project
        delete_project_parser = subparsers.add_parser("delete-project")
        delete_project_parser.add_argument('project_id', type=int, help="ID of the project to delete")
        delete_project_parser.set_defaults(func=self.handle_delete_project)
        
        #add task
        task_parser = subparsers.add_parser("add-task")
        task_parser.add_argument('project_id', type=int, help="Id of project assigned to the task")
        task_parser.add_argument('title', help = "Title of the task")
        task_parser.add_argument('status', help="Completed or Incomplete")
        task_parser.add_argument('assigned_to', help="Email of the user assigned to the task")
        task_parser.set_defaults(func=self.handle_add_task)
        
        #complete task
        completed_task_parser = subparsers.add_parser("mark-task-as-complete")
        completed_task_parser.add_argument('task_id', type=int, help="Id of the task to mark as complete")
        completed_task_parser.set_defaults(func=self.handle_completed_task)
        
        
        
    #handler methods
    def handle_add_user(self, args):
        #adding new user
        User(name=args.name, email=args.email)
        User.save_users_to_file()
        print(f"User {args.name} created")
    
    def list_users(self, args):
        if not User.users:
            print("No users found.")
            return
        
        print("\n--- Current Users ---")
        table_data = []
        for person in User.users:
            table_data.append([person.name, person.email])
        print(tabulate(table_data, headers=["Name", "Email"], tablefmt="grid"))
        
    def handle_add_project(self, args):
        user_exists = any(user.email == args.owner_email for user in User.users)
        if not user_exists:
            print(f"Error: No user with email {args.owner_email} found.")
            return
        
        Project(title=args.title, description=args.description, due_date=args.due_date, owner_email=args.owner_email)
        Project.save_projects_to_file()
        print(f"Project '{args.title}' created")
        
    def handle_list_projects(self, args):
        user_projects = [project for project in Project.projects if project.owner_email == args.user]
        if not user_projects:
            print(f"No projects found for user with email {args.user}.")
            return
        
        print(f"\n--- Projects for {args.user} ---")
        table_data = []
        for project in user_projects:
            table_data.append([project.id, project.title, project.description, project.due_date])
        print(tabulate(table_data, headers=["ID", "Title", "Description", "Due Date"], tablefmt="grid"))
        
    def handle_delete_project(self, args):
        project_to_delete = next((project for project in Project.projects if project.id == args.project_id), None)
        if not project_to_delete:
            print(f"Error: No project with ID {args.project_id} found.")
            return
        
        Project.projects.remove(project_to_delete)
        Project.save_projects_to_file()
        print(f"Project with ID {args.project_id} deleted successfully.")
        
    def handle_add_task(self, args):
        find_project = any(project.id == args.project_id for project in Project.projects)
        if not find_project:
            print(f"Error: Project with ID {args.project_id} not found.")
            return
        
        find_user = any(user.email == args.assigned_to for user in User.users)
        if not find_user:
            print(f"Error: User with email {args.assigned_to} not found.")
            return
        Task(project_id=args.project_id, title=args.title, status=args.status, assigned_to=args.assigned_to)
        Task.save_to_file()
        print(f"✅ Task '{args.title}' added to Project {args.project_id}.")
        
    
    def handle_completed_task(self, args):
        task_to_complete = next((task for task in Task.tasks if task.id == args.task_id), None) 
        
        if not task_to_complete:
         print(f"❌ Error: No task found with ID {args.task_id}")
         return
        
        task_to_complete.mark_as_complete()
        print(f"✅ Task {args.task_id} ('{task_to_complete.title}') marked as Complete!")
        Task.save_to_file()
            
    def start(self):
        args = self.parser.parse_args()
        if hasattr(args, 'func'):
            args.func(args)
        else:
            self.parser.print_help()

def main():
    cli = CLI()
    cli.start()
    
if __name__ == "__main__":
    main()
