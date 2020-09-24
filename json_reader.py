"""Functions relating to opening json file are contained here.

json module is used.
"""


# Import required modules
import json


# Done by Jun Hong
def read_file(file_name):
    """Takes in 'file_name' string and return the file content.

    Function read_file(file_name) takes in a 'file_name' of string type, opens the file with open() of json module,
    loads the file with load() of json module, assigns file contents into 'data' and returns 'data'. 'data' type
    depends on the file content.
    """

    # Open file to read and return file contents
    with open(file=file_name) as json_file:
        data = json.load(fp=json_file)
    return data
