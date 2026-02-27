import json
from utils.storage_handler import save_to_file, load_from_file

class User:
    users = []
    users_data = "data/users.json"
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        
        User.users.append(self)
    
    #to ensure clean output
    def __str__(self):
        return f"User: '{self.name}', | Email: '{self.email}'"
    
    @classmethod
    def read_from_file(cls):
        try:
        
            data = load_from_file(cls.users_data)
            cls.users = []
                
            if data is None:
                print("No user data found. Starting with an empty list.")
                return
            for user in data:
                cls(name = user['name'], email = user['email'])
        except FileNotFoundError:
            print("Data file not found")
            cls.users = []
        #handles if the file exists but is empty or corrupted
        except json.JSONDecodeError:
            print("users.json is corrupted.Starting with an empty list")
            cls.users = []
                    
                
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
            
       