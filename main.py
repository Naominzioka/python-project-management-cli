from models.user import User
from models.project import Project
import argparse
from tabulate import tabulate

#main function
class CLI:
    def __init__(self):
        User.read_from_file()
        self.parser = argparse.ArgumentParser(description="Project Manager CLI")
        subparsers = self.parser.add_subparsers(dest="command")
        
        #add-user command
        user_parser = subparsers.add_parser("add-user")
        user_parser.add_argument('name', help="Name of user")
        user_parser.add_argument('email', help="Email address of user")
        user_parser.set_defaults(func=User)
        #list command
        subparsers.add_parser("list-users")
        
        #project commands
        project_parser = subparsers.add_parser("add-project")
        project_parser.add_argument('title', help="Name of project")
        project_parser.add_argument('description', help="Description of project")
        project_parser.add_argument('due_date', help="Due date of project")
        project_parser.set_defaults(func=Project)
        
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
            table_data = []
            for person in User.users:
                table_data.append([person.name, person.email])
            print(tabulate(table_data, headers=["Name", "Email"], tablefmt="grid"))
            
        elif args.command == 'add-project':
            Project(title=args.title, description=args.description, due_date=args.due_date)
            print(f"Project {args.title} created")
                
        elif args.command is None:
            self.parser.print_help()
    

def main():
    app = CLI()
    app.start()          
              
              
if __name__ == "__main__":
    main()