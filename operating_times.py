"""Functions relating to 'Operating Time.json' file are contained here.

Data from 'Operating Time.json' are taken from https://www.ntu.edu.sg/has/FnB/Pages/NorthSpine.aspx.
"""


# Import required modules
from day_time import check_day, compare_time, get_current_day, get_current_time, return_day_tuple
from json_reader import read_file

# Initialise required variables
all_operating_times = read_file(file_name='Operating Times.json')
closed_str = 'Closed'
stalls_display_str = 'Stalls'


# Done by Jun Hong
def check_stall_opened(stall, user_day=get_current_day(), user_time=get_current_time()):
    """Returns a boolean of whether the stall is open, given strings 'stall', 'user_day', 'user_time'.

    Function check_stall_opened(stall, user_day, user_time) takes in 'stall' string, along with optional 'user_day'
    and 'user_time' strings(uses current day and time otherwise). The function then checks whether the stall is open
    by comparing it with 'all_operating_times' dictionary using check_day() and compare_time() functions. True is
    returned if the stall is open, False otherwise.
    """

    # Iterate through the stall to check whether stall is open
    for (key, value) in all_operating_times[stall].items():
        if check_day(day=key) and value != closed_str:
            all_timings = value.split(sep='/')
            for timing in all_timings:
                if compare_time(user_time=user_time, time_range=timing) and user_day in return_day_tuple(day_type=key):
                    return True
    return False


# Done by Jun Hong
def get_operating_time(stall):
    """Returns a string with operating times of given string 'stall', nicely formatted.

    Function get_operating_time(stall) takes in 'stall' string. The function then retrieves the stall name and
    operating times from 'all_operating_times' dictionary and sort them nicely into a string. The string is then
    returned.
    """

    # Initialise string
    stall_operating_time_str = 'Operating Hours'

    # Add stall operating times
    for (key, value) in all_operating_times[stall].items():
        if check_day(day=key):
            stall_operating_time_str += '\n\n' + key + '\n' + value
    return stall_operating_time_str


# Done by Jun Hong
def get_operating_times():
    """Returns a string with operating times of all stalls, nicely formatted.

    Function get_operating_times() calls get_operating_time(stall) for ever stall in 'all_operating_times'. The
    string from get_operating_time(stall) is combined and returned.
    """

    # Initialise string
    stalls_operating_time_str = stalls_display_str

    # Format string nicely
    for stall in all_operating_times:
        stalls_operating_time_str += '\n\n' + get_operating_time(stall=stall)
    return stalls_operating_time_str


# Done by Jun Hong
def get_stall_info(stall):
    """Returns a string with information of given string 'stall', nicely formatted.

    Function get_stall_info(stall) takes in 'stall' string. The function then retrieves the stall name, address,
    operating times and more from 'all_operating_times' dictionary and sort them nicely into a string. The string is
    then returned.
    """

    # Initialise string
    stall_info_str = stall

    # Add stall info
    for (key, value) in all_operating_times[stall].items():
        stall_info_str += '\n' + key + ' ' + value
    return stall_info_str


# Done by Jun Hong
def get_stalls_info():
    """Returns a string with information of all stalls, nicely formatted.

    Function get_stalls_info() calls get_stall_info(stall) for every stall in 'all_operating_times'. The strings from
    get_stall_info(stall) is then combined and returned.
    """

    # Initialise string
    stalls_info_str = stalls_display_str

    # Format string nicely
    for stall in all_operating_times:
        stalls_info_str += '\n\n' + get_stall_info(stall=stall)
    return stalls_info_str


# Done by Jun Hong
def get_waiting_time(stall):
    """Returns waiting time multiplier of a given 'stall' string.

    Function get_waiting_time(stall) takes in 'stall' string and returns the multiplier of waiting time
    """

    # Returns the stall's waiting time
    return all_operating_times[stall]['Waiting Time']
