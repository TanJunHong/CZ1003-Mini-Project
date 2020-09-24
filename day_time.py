"""Functions relating to day and time are contained here.

datetime module is used. Data from 'Public Holiday.json' are taken from
https://rjchow.github.io/singapore_public_holidays/api/**<year>**/data.json.
"""


# Import required modules
from datetime import datetime
from json_reader import read_file

# Initialise required variables
day_type_dictionary = {'Weekday': ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'),
                       'Weekend': ('Saturday', 'Sunday'),
                       'Public Holiday': 'Public Holiday', }
public_holiday = read_file(file_name='Public Holiday.json')


# Done by Jun Hong
def check_day(day):
    """Returns a boolean of if the given 'day' string is valid day/day type'.

    Function check_day(day) takes in string 'day_type' and check if it is a valid day or day/type. For example,
    it will check whether it is a weekday or weekend, or a day in a weekday or weekend. It will return True if it is,
    otherwise False.
    """

    # Check whether the day in a valid day type
    for day_tuple in day_type_dictionary.values():
        if day in day_tuple:
            return True
    return day in day_type_dictionary


# Done by Jun Hong
def convert_date(user_date_input):
    """Returns time converted from given 'user_date_input' string input.

    Function convert_date(user_date_input) takes in string 'user_date_input' and converts to datetime.datetime using
    strptime() of datetime module. The datetime.datetime is then returned.
    """

    # Convert date string into datetime
    return datetime.strptime(user_date_input, '%d/%m/%Y')


# Done by Jun Hong
def convert_time(user_time_input):
    """Returns time converted from given 'user_time_input' string input.

    Function convert_time(user_time_input) takes in string 'user_time_input' and converts to datetime.datetime using
    strptime() of datetime module. The datetime.datetime is then returned.
    """

    # Convert time string into datetime
    return datetime.strptime(user_time_input, "%H:%M")


# Done by Jun Hong
def return_day_tuple(day_type):
    """Returns a tuple of days of 'day_type' type, given string 'day_type'.

    Function return_day_tuple(day_type) takes in string 'day_type' and check if it is Weekday, Weekend or Public
    Holiday. It will return a tuple of days in weekday, weekend or public holiday. It will return itself in a tuple
    otherwise.
    """

    # Return the tuple of days in day type
    if day_type in day_type_dictionary:
        return day_type_dictionary[day_type]
    return day_type,


# Done by Jun Hong
def get_current_day():
    """Returns current day in string.

    Function get_current_day() retrieves a day string using strftime() and datetime.now() of datetime module. The
    string is then returned. (Checks for Public Holiday too)
    """

    # Return current day or public holiday if current day is public holiday
    if check_public_holiday():
        return 'Public Holiday'
    return datetime.now().strftime(format='%A')


# Done by Jun Hong
def get_current_date():
    """Returns current date in string.

    Function get_current_date() retrieves a date string using strftime() and datetime.now() of datetime module. The
    string is then returned.
    """

    # Get current date and return date string
    return datetime.now().strftime(format='%d/%m/%Y')


# Done by Jun Hong
def get_current_time():
    """Returns current time in string.

    Function get_current_time() retrieves a time string using strftime() and datetime.now() of datetime module. The
    string is then returned.
    """

    # Get current time and return time string
    return datetime.now().strftime(format='%H:%M')


# Done by Jun Hong
def get_current_time_in_seconds():
    """Returns current time in seconds in string.

    Function get_current_time() retrieves a time string with seconds using strftime() and datetime.now() of datetime
    module. The string is then returned.
    """

    # Get current time and return time string with seconds
    return datetime.now().strftime(format='%H:%M:%S')


# Done by Jun Hong
def get_day(user_date):
    """Returns given 'user_date' day in string.

    Function get_day(user_date) retrieves a day string using strftime() and datetime.now() of datetime module. The
    string is then returned. (Checks for Public Holiday too)
    """

    # Return the day itself or public holiday
    if check_public_holiday(user_date=user_date.strftime(format='%d/%m/%Y')):
        return 'Public Holiday'
    return user_date.strftime(format='%A')


# Done by Jun Hong
def check_public_holiday(user_date=None):
    """Returns whether 'user_date' string is a public holiday.

    Function check_public_holiday(user_date) takes in string 'user_date' (optional, will use current date otherwise).
    The string is then compared with 'public_holiday' list to see if it is a public holiday. Returns True if it is a
    holiday, False otherwise.
    """

    # Use current date with no date specified
    if user_date is None:
        user_date = get_current_date()

    # Convert string to datetime
    date = datetime.strptime(user_date, '%d/%m/%Y')

    # Check if day is in public holiday data
    for public_holiday_dict in public_holiday:
        if date == datetime.strptime(public_holiday_dict['Observance'], '%d/%m/%Y'):
            return True
    return False


# Done by Jun Hong
def compare_time(user_time=get_current_time(), time_range='00:00-23:59'):
    """Returns whether 'user_time' is within 'time_range', given both in strings

    Function compare_time(user_time, time_range) takes in strings 'user_time' and 'time_range' (optional,
    uses current time and full time range otherwise). The strings are then converted to datetime.time format using
    strptime() and time() of datetime module and compared to see if user time is within the range. True is returned
    if it is, False otherwise.
    """

    # Separate start and end time
    start_time, end_time = time_range.split(sep='-')

    # Compare time to see if its within start and end time
    return datetime.strptime(start_time, '%H:%M').time() \
        <= datetime.strptime(user_time, '%H:%M').time() \
        <= datetime.strptime(end_time, '%H:%M').time()
