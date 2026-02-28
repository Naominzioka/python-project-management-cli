from models.user import User
from models.project import Project
from models.task import Task
from cli_parser import setup_parser

def main():
    #load existing data
        User.read_from_file()
        Project.read_from_file()
        Task.read_from_file()
        
        parser = setup_parser()
        args = parser.parse_args()
        
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()
    
    
    
if __name__ == "__main__":
    main()
