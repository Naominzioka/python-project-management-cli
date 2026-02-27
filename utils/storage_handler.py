import json
import os

#this file handles the DRY principle for file handling.
# It has two functions, one to save data to a file and another to load data from a file. 
# This way, we can reuse these functions across different models without repeating the same code.

def save_to_file(data, filename):
    # Ensure the directory exists before trying to save the file
    #if data folder is not available, it creates it. exist_ok=True prevents an error if the directory already exists.
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Convert the list of objects to a list of dictionaries for better readability in the JSON file
        data_saved = []
        for item in data:
            if isinstance(item, dict):
                data_saved.append(item)
            elif hasattr(item, "to_dict"):
                data_saved.append(item.to_dict())
            else:
                data_saved.append(item.__dict__)
        
        #opening with 'w' creates the file if it does not exist and allows us to write to it. The json.dump function is used to write the data to the file in JSON format.
        with open(filename, "w") as file:
            #indent=4 adds indentation for better readability of the JSON file, json dump converts the list of dictionaries to a
            # JSON formatted string and writes it to the file.
            json.dump(data_saved, file, indent=4)
            

def load_from_file(filename):
    if not os.path.exists(filename):
        return None
    #read the file and return data as a python object.
    with open(filename, "r") as file:
        return json.load(file)
    
    
    