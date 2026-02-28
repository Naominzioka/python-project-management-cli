import argparse
import handlers


def setup_parser():
        parser = argparse.ArgumentParser(description="Project Manager CLI")
        subparsers = parser.add_subparsers(dest="command")
        
        #add user    
        user_parser = subparsers.add_parser("add-user")
        user_parser.add_argument('name', help="Name of user")
        user_parser.add_argument('email', help="Email address of user")
        user_parser.set_defaults(func=handlers.handle_add_user)
        
        #list users
        list_users_parser = subparsers.add_parser("list-users")
        list_users_parser.set_defaults(func=handlers.list_users)
        
        #add project
        project_parser = subparsers.add_parser("add-project")
        project_parser.add_argument('title', help="Name of project")
        project_parser.add_argument('description', help="Description of project")
        project_parser.add_argument('due_date', help="Due date of project -Format: YYYY-MM-DD")
        project_parser.add_argument('owner_email', help="Email of the project owner")
        project_parser.set_defaults(func=handlers.handle_add_project)
        
        #list projects
        list_project_parser = subparsers.add_parser("list-projects")
        list_project_parser.add_argument('user', help="Email of the user associated with a certain project")
        list_project_parser.set_defaults(func=handlers.handle_list_projects)
        
        #delete project
        delete_project_parser = subparsers.add_parser("delete-project")
        delete_project_parser.add_argument('project_id', type=int, help="ID of the project to delete")
        delete_project_parser.set_defaults(func=handlers.handle_delete_project)
        
        #add task
        task_parser = subparsers.add_parser("add-task")
        task_parser.add_argument('project_id', type=int, help="Id of project assigned to the task")
        task_parser.add_argument('title', help = "Title of the task")
        task_parser.add_argument('status', help="Completed or Incomplete")
        task_parser.add_argument('assigned_to', help="Email of the user assigned to the task")
        task_parser.set_defaults(func=handlers.handle_add_task)
        
        #complete task
        completed_task_parser = subparsers.add_parser("mark-task-as-complete")
        completed_task_parser.add_argument('task_id', type=int, help="Id of the task to mark as complete")
        completed_task_parser.set_defaults(func=handlers.handle_completed_task)
    
        return parser
        
        