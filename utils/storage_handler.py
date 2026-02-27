import json
import os

#this file handles the DRY principle for file handling.
# It has two functions, one to save data to a file and another to load data from a file. 
# This way, we can reuse these functions across different models without repeating the same code.

def save_to_file(data, filename):
    # Ensure the directory exists before trying to save the file
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        #convert list of objects to a list of dictionaries for better readability in the JSON file
        dict_data = [obj.__dict__ for obj in data]
        with open(filename, "w") as file:
            #indent=4 adds indentation for better readability of the JSON file, 
            # json dump converts the list of dictionaries to a
            # JSON formatted string and writes it to the file.
            json.dump(dict_data, file, indent=4)
            

def load_from_file(filename):
    if not os.path.exists(filename):
        return None
    
    with open(filename, "r") as file:
        return json.load(file)
    
    
    