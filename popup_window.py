"""Second Window

All of the second window related items are here.
"""

# Import required modules
from day_time import get_current_day, get_current_time
from menu import get_menu, get_stalls
from operating_times import check_stall_opened, get_operating_time, get_waiting_time
from random import randint
from tkinter import Button, Label, messagebox, PhotoImage, simpledialog, Toplevel

# Initialise required variables
map_stalls_list = get_stalls()
title = 'NTU'

user_day = get_current_day()
user_time = get_current_time()


# Done by Chin Yi
def back(root, me):
    """Goes Back to main page, given 'root' and 'me'.

    Function back(root,me) takes in 'root' and 'me', destroys 'me' and shows 'root'
    """

    me.destroy()
    root.deiconify()


# Done by Chin Yi
def centre_window(window):
    """Centres main window given 'window'

    Function centre_window(window) centres the given 'window' by taking into account main window geometry and screen
    geometry. winfo_screenwidth(), winfo_screenheight(), winfo_width(), winfo_height() are used. The main window is
    hidden using withdraw() then displayed again using deiconify().
    """

    # Hide window
    window.withdraw()

    # Update
    window.update_idletasks()

    # Calculations to centre the window
    x = (window.winfo_screenwidth() - max(window.winfo_width(), window.winfo_reqwidth())) / 2
    y = (window.winfo_screenheight() - max(window.winfo_height(), window.winfo_reqheight())) / 2
    window.geometry(newGeometry='+%d+%d' % (x, y))

    # Show window
    window.deiconify()


# Done by Chin Yi
def create_elements(counter, mini_window, main_window):
    """Create all the elements in the main_window given 'counter' int, mini_window and main_window.

    Function create_elements(counter, mini_window, main_window) takes in 'counter' int, mini_window and main_window.
    It creates the necessary elements for the second window.
    """

    # Initialise required variables
    bg = 'beige'
    color = 'Blue'
    stall = map_stalls_list[counter]

    # Waiting Time Algorithm
    no_of_ppl_in_queue = randint(a=5, b=7)
    waiting_time_random = no_of_ppl_in_queue * get_waiting_time(stall=stall)

    # Done by Jun Hong
    def update(hour_glass_index=0):
        """Changes the picture every defined 'period' ms, given 'hour_glass_index' int (default is 0).

        Function update(hour_glass_index) takes in int 'hour_glass_index', and increments it every 'period' ms and
        changes the image. (default of hour_glass_index is 0)
        """

        # Initialise required variables
        period = 50

        # Waiting time button image
        hour_glass_frame = hour_glass_frames[hour_glass_index]
        waiting_time_button.configure(image=hour_glass_frame)
        waiting_time_button.image = hour_glass_frame

        # Increment hour_glass_index
        hour_glass_index += 1
        if hour_glass_index > 95:
            hour_glass_index = 0

        # Call itself again
        mini_window.after(ms=period, func=lambda index=hour_glass_index: update(hour_glass_index=index))

    # Waiting Time Button
    waiting_time_text = 'Current waiting time: %d mins.\n\n(Enter the no. of people in\n queue now to get waiting ' \
                        'time!)' % waiting_time_random
    waiting_time_button = Button(master=mini_window, compound='bottom', font=('Arial', 15), bd=2, fg='dark slate blue',
                                 borderwidth=0, activebackground=color, activeforeground=color, bg=bg, state='disabled',
                                 command=lambda: waiting_time(stall=stall))
    if check_stall_opened(stall=stall, user_time=user_time, user_day=user_day):
        waiting_time_button.configure(state='normal', text=waiting_time_text)
    waiting_time_button.grid(row=0, column=0, sticky='nsew')

    # Operating Hours Label
    operating_hours_label = Label(master=mini_window, text=get_operating_time(stall=stall), font=('Arial', 20), bg=bg,
                                  fg='green', compound='bottom')
    operating_hours_label.grid(row=1, column=0, sticky='nsew')

    # Stall Menu Label
    background_image = PhotoImage(file='image\\Background.png')
    menu_label = Label(master=mini_window, font=('Arial', 30), bg='black', fg='green')
    menu_label.configure(text=get_menu(stall=stall, user_day=user_day, user_time=user_time), borderwidth=0,
                         compound='center', image=background_image)
    menu_label.image = background_image
    menu_label.grid(row=0, column=1, rowspan=2, sticky='nsew')

    # Animated GIF
    hour_glass_frames = [PhotoImage(file='image\\hour_glass\\frame(' + str(object=i + 1) + ').png') for i in range(96)]
    mini_window.after(ms=0, func=update)

    # Back Button
    back_button_image = PhotoImage(file="image\\back button.png")
    back_button = Button(master=menu_label, image=back_button_image, activebackground=color, activeforeground=color,
                         command=lambda root=main_window, me=mini_window: back(root=main_window, me=mini_window), bd=2)
    back_button.image = back_button_image
    back_button.place(relx=0.875, rely=0.88, anchor='center')


# Done by Chin Yi
def input_time(day, time):
    """Given 'day' and 'time' strings, store them.

    Function input_time takes in 'day' and 'time' strings and store them in the global variables.
    """

    # Update global variables
    global user_day, user_time
    user_day = day
    user_time = time


# Done by Chin Yi
def initialise(counter, main_window):
    """Initialise main window given 'main_window' and 'counter' int.

    Function initialise(counter, main_window) takes in 'main_window' and 'counter' int and calls create_elements().
    """

    # Initialise window
    mini_window = Toplevel()

    # Make window not resizable
    mini_window.resizable(height=0, width=0)

    # Remap close button to go back to previous window
    close = 'WM_DELETE_WINDOW'
    mini_window.protocol(func=lambda root=main_window, window=mini_window: back(root=main_window, me=mini_window),
                         name=close)

    # Call create element
    create_elements(counter=counter, mini_window=mini_window, main_window=main_window)

    # Centres window
    centre_window(window=mini_window)


# Done by Chin Yi
def waiting_time(stall):
    """Shows a dialog asking for number of people in queue and returns estimated waiting time given 'stall' string.

    Function waiting_time(stall) shows a simple dialog asking for a integer input, and returns estimated waiting time.
    The 'stall' string is used to retrieve the stall's multiplier.
    """

    # Loop until valid input or cancel
    while True:

        # Get user's input
        people = simpledialog.askinteger(title=title, prompt='Enter Number of People in Queue', minvalue=0)

        # Show waiting time
        if people is not None:
            message = 'Waiting time is about ' + str(object=round(number=people * get_waiting_time(stall=stall))) + \
                      ' mins.'
            messagebox.showinfo(title=title, message=message)
        break
