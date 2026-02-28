import json, os
from models.person import Person
from utils.storage_handler import save_to_file, load_from_file

class User(Person):
    users = []
    users_data = "data/users.json"
    
    def __init__(self, name, email):
        #inherits name and email from person class
        super().__init__(name, email)
        
        User.users.append(self)
        
    def to_dict(self):
        #inherits name and email from person class and returns them in a dictionary format for saving to json file
        return {
            "name": self.name,
            "email": self.email
        }

        #to ensure clean output
    def __str__(self):
        return f"User: '{self.name}', | Email: '{self.email}'"
    

    
    @classmethod
    def read_from_file(cls):
        #check if the file exists first
        if not os.path.exists(cls.users_data):
            cls.users = []
            return
        try:
        
            data = load_from_file(cls.users_data)
            cls.users = []
                
            if data is None:
                print("No user data found. Starting with an empty list.")
                return
            for user in data:
                cls(name = user['name'], email = user['email'])
                
        #handles if the file exists but is empty or corrupted
        except json.JSONDecodeError:
            print("users.json is corrupted.Starting with an empty list")
            cls.users = []
                    
        except Exception as e:
            print(f"Error loading file: {e}")
        
        
                
    @classmethod
    def save_users_to_file(cls):
        try:
            save_to_file(cls.users, cls.users_data)
            users_saved = []
            for user in cls.users:
                users_saved.append({"name": user.name,
                                    "email": user.email})
            print(f"✅ User saved to {cls.users_data}")
        except PermissionError:
            print(f"Error: Permission denied when writing to {cls.users_data}")
        except OSError as e:
            #for errors like disk full
            print(f"❌ System Error: {e}")
        except Exception as e:
            #for any other unexpected bugs
            print(f"❌ An unexpected error occurred: {e}")
            