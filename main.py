from models.user import User
from models.project import Project
import argparse
from tabulate import tabulate

#main function
class CLI:
    def __init__(self):
        User.read_from_file()
        Project.read_from_file()
        self.parser = argparse.ArgumentParser(description="Project Manager CLI")
        subparsers = self.parser.add_subparsers(dest="command")
        
        #subparser for user commands
        user_parser = subparsers.add_parser("add-user")
        user_parser.add_argument('name', help="Name of user")
        user_parser.add_argument('email', help="Email address of user")
        user_parser.set_defaults(func=User)
        #list command
        subparsers.add_parser("list-users")
        
        #subparsers for project commands
        project_parser = subparsers.add_parser("add-project")
        project_parser.add_argument('title', help="Name of project")
        project_parser.add_argument('description', help="Description of project")
        project_parser.add_argument('due_date', help="Due date of project -Format: YYYY-MM-DD")
        project_parser.add_argument('owner_email', help="Email of the project owner")
        project_parser.set_defaults(func=Project)
        list_project_parser = subparsers.add_parser("list-projects")
        list_project_parser.add_argument('user', help="Filter projects by user email")
        #subparsers for delete project command
        delete_project_parser = subparsers.add_parser("delete-project")
        delete_project_parser.add_argument('project_id', type=int, help="ID of the project to delete")
        delete_project_parser.set_defaults(func=Project)
        
        
    def start(self):
        args = self.parser.parse_args()
        
        if args.command == 'add-user':
            User(name=args.name, email=args.email)
            User.save_users_to_file()
            print(f"User {args.name} created")
            
        elif args.command == 'list-users':
            if not User.users:
                print("No users found.")
                return
            
            print("\n--- Current Users ---")
            #pretty printing in table format using the tabulate library imported at the top
            table_data = []
            for person in User.users:
                table_data.append([person.name, person.email])
            print(tabulate(table_data, headers=["Name", "Email"], tablefmt="grid"))
            
        elif args.command == 'add-project':
            user_exists = any(user.email == args.owner_email for user in User.users)
            if not user_exists:
                print(f"Error: No user with email {args.owner_email} found.")
                return
            Project(title=args.title, description=args.description, due_date=args.due_date, owner_email=args.owner_email)
            Project.save_projects_to_file()
            print(f"✅ Project {args.title} created successfully.")
            
        elif args.command == 'list-projects':
            user_projects = [project for project in Project.projects if project.owner_email == args.user]
            if not user_projects:
                print(f"No projects found for user with email {args.user}.")
                return
            
            print(f"\n--- Projects for User {args.user} ---")
            #uses the tabulate library imported at the top for pretty printing in table format
            table_data = []
            for project in user_projects:
                table_data.append([project.title, project.description, project.due_date])
            print(tabulate(table_data, headers=["Title", "Description", "Due Date"], tablefmt="grid"))
            
        elif args.command == 'delete-project':
            success = Project.delete_project(args.project_id)
            
            if success:
                print(f"Project with ID {args.project_id} has been deleted.")
            else:
                print(f"No project found with ID {args.project_id}.")
            
        elif args.command is None:
            self.parser.print_help()
    

def main():
    app = CLI()
    app.start()          
              
              
if __name__ == "__main__":
    main()