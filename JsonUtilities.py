import json

def json_to_obj(filename):
    """Extracts dta from JSON file and saves it on Python object
    """
    obj = None
    with open(filename) as json_file:
        obj = json.loads(json_file.read())
    return obj
 
 
def save_data(data,filename):
    """Converts data to JSON.
    """
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


    