"""Main Window

All of the main window related items are here.
"""

# Import required modules
from day_time import get_current_date, get_current_time, get_current_time_in_seconds, get_day, get_current_day
from menu import get_number_of_stalls, get_stalls
from operating_times import check_stall_opened
from popup_window import centre_window, input_time, initialise
from tkcalendar import Calendar
from tkinter import Button, Canvas, Label, OptionMenu, PhotoImage, Tk, Toplevel, StringVar

# Initialise required variables
title = 'North Spine Plaza'
geometry = '1024x660'
image_str = 'image\\'
image_format = '.png'
font = 'MSGothic 20 bold'
anchor = 'center'
frame = 'frame'
grey = ' (Grey)'
time_id = None

frame_position_list = ((0.562, 0.357), (0.715, 0.645), (0.702, 0.148), (0.561, 0.551), (0.7095, 0.3705))
user_day = get_current_day()
user_time = get_current_time()

GUI = Tk()

pin_label_list = []
pin_image_list = []

background_canvas = Canvas(master=GUI, highlightthickness=0, borderwidth=0)
map_canvas = Canvas(master=GUI, highlightthickness=100, borderwidth=100)
poster_canvas = Canvas(master=GUI, highlightthickness=0, borderwidth=0)
stall_label_list = [Label(master=GUI, highlightthickness=5, borderwidth=5, bg='cyan') for i in get_stalls()]


# Done by Venkat
def click(event, window, item_id):
    """Hides first window, shows 2nd window on click, given which label is clicked, given 'window' and 'item_id' int.

    Function click(event, window, item_id) takes in 'window' and 'item_id' int, hides the first window and shows the 2nd
    window.
    """

    # Call 2nd Window
    initialise(counter=item_id, main_window=window)

    # Hide this window
    window.withdraw()


# Done by Venkat
def initialize(window):
    """Initialise main window given 'window'.

    Function initialize(window) takes in 'window' and initialises the main window and calls create_elements().
    """

    # Create elements
    create_elements(window=window)

    # Main window
    window.configure(highlightthickness=0, borderwidth=0)
    window.title(string=title)
    window.geometry(newGeometry=geometry)
    centre_window(window=window)
    window.mainloop()


# Done by Venkat
def input_specific_time():
    """Create a new window to allow the user to input date and time.

    Function input_specific_time() uses tkcalendar to get user's date and drop down menu to get user's time.
    """

    # Done by Venkat
    def change_datetime():
        """Change date and time based on input

        Function change_datetime() displays the user's date and time, and changes the stored day and time.
        """

        # Use global variables
        global user_time, user_day, time_id

        # Initialise required variables
        datetime_format = 'Selected Date and Time: %d/%m/%Y, '
        user_time = hour_variable.get() + ':' + minute_variable.get()
        user_day = get_day(user_date=calendar.selection_get())
        user_date = calendar.selection_get()

        # Change day and time for second window
        input_time(day=user_day, time=user_time)

        # Check whether the text exist, if it exist then modify, else create the text first.
        if time_id is None:
            time_id = background_canvas.create_text((GUI.winfo_width() / 2, 50), font=font, anchor=anchor, fill='white')
        background_canvas.itemconfigure(tagOrId=time_id, text=user_date.strftime(format=datetime_format) + user_time)

        # Closes the window
        top.destroy()

    # Done by Venkat
    def reset():
        """Reset the date and time to current date and time.

        Function reset() replaces the date and time to current date and time and store it.
        """

        # Use and reset global variables
        global user_time, user_day, time_id
        user_time = get_current_time()
        user_day = get_current_day()

        # Change day and time for second window
        input_time(day=user_day, time=user_time)

        # Remove the Label
        background_canvas.delete(time_id)
        time_id = None

        # Closes the window
        top.destroy()

    # Initialise required variables
    clock_font = ('Arial', 20)
    string_format = '{:02d}'
    default_value = '00'
    fill = 'both'

    # Calendar
    top = Toplevel()
    calendar = Calendar(master=top, font='Arial 14', selectmode='day', locale='en_SG', cursor='hand2')
    calendar.pack(fill=fill, expand=True)

    # Hours
    top_canvas = Canvas(master=top)
    hours_list = [string_format.format(i) for i in range(24)]
    hour_variable = StringVar(master=top_canvas)
    hour_variable.set(value=default_value)
    hour_option = OptionMenu(top_canvas, hour_variable, *hours_list)
    hour_option.config(font=clock_font)
    hour_option.grid(row=0, column=0)

    # Colon
    colon_label = Label(master=top_canvas, text=':', font=clock_font)
    colon_label.grid(row=0, column=1)

    # Minutes
    minutes_list = [string_format.format(i) for i in range(0, 60, 15)]
    minute_variable = StringVar(master=top_canvas)
    minute_variable.set(value=default_value)
    minute_option = OptionMenu(top_canvas, minute_variable, *minutes_list)
    minute_option.config(font=clock_font)
    minute_option.grid(row=0, column=2)
    top_canvas.pack()

    # OK Button
    ok_button = Button(master=top, text='OK', command=change_datetime)
    ok_button.pack(fill=fill)

    # Reset Button
    reset_button = Button(master=top, text='Reset', command=reset)
    reset_button.pack(fill=fill)
    centre_window(window=top)


# Done by Venkat
def create_elements(window):
    """Create all the elements in the main_window given 'window'.

    Function create_elements(window) takes in 'window' creates and configures background_canvas, map_canvas, map_label,
    ntu_logo, clock(calling update_time_label(clock_id)), time_button and calls create_hover_labels().
    """

    # Background
    background_image = PhotoImage(file=image_str + 'The Hive' + image_format)
    background_canvas.create_image(800, 650, image=background_image, anchor=anchor)
    window.image = background_image
    background_canvas.place(x=0, y=0, relwidth=1, relheight=1)

    # NTU Map
    map_canvas.place(relx=0.68, rely=0.57, anchor=anchor)
    map_image = PhotoImage(file=image_str + 'NTU Map' + image_format)
    map_label = Label(master=map_canvas, image=map_image, highlightthickness=0, borderwidth=0)
    map_label.image = map_image
    map_label.pack()

    # Poster on the left
    poster_canvas.place(relx=0.20, rely=0.57, anchor=anchor)
    poster_image = PhotoImage(file=image_str + 'Poster' + image_format)
    poster_label = Label(master=poster_canvas, image=poster_image, highlightthickness=0, borderwidth=0)
    poster_label.image = poster_image
    poster_label.pack()

    # NTU Logo
    ntu_logo = PhotoImage(file=image_str + 'NTU Logo' + image_format)
    background_canvas.create_image((130, 50), image=ntu_logo)
    background_canvas.image = ntu_logo

    # Clock
    clock_id = background_canvas.create_text((window.winfo_width() - 100, 50), font=font, anchor=anchor, justify=anchor)
    window.bind('<Configure>', lambda event, item_id=clock_id: move(event, window=window, clock_id=item_id))
    update_time_label(clock_id=clock_id)

    # Hover Labels
    create_hover_labels(window=window)

    # Time Button
    time_image = PhotoImage(file=image_str + 'Clock' + image_format)
    time_button = Button(master=poster_canvas, image=time_image, activebackground='Blue', activeforeground='Blue',
                         font='30')
    time_button.configure(command=lambda: input_specific_time())
    time_button.image = time_image
    time_button.place(relx=0.25, rely=0.51, anchor=anchor)


# Done by Venkat
def create_hover_labels(window):
    """Creates all hover labels and its images and bind them to the label, given 'window'.

    Function create_hover_labels(window) takes in 'window' and creates and configures pin_label_list labels and
    pin_image_list images.
    """

    # Iterate to generate items
    for i in range(get_number_of_stalls()):

        # Pin Images
        pin_image_list.append(PhotoImage(file=image_str + frame + str(i + 1) + image_format))

        # Pin Labels
        pin_label_list.append(Label(master=map_canvas, image=pin_image_list[i], highlightthickness=0, borderwidth=0))
        pin_label_list[i].place(relx=frame_position_list[i][0], rely=frame_position_list[i][1], anchor=anchor)
        pin_label_list[i].bind('<Button-1>', lambda event, root=window, item=i: click(event, window=root, item_id=item))
        pin_label_list[i].bind('<Enter>', lambda event, root=window, item=i: hover(event, window=root, item_id=item))
        pin_label_list[i].bind('<Leave>', leave)


# Done by Venkat
def hover(event, window, item_id):
    """When hovered, shows image of the stall (Grey if closed, Coloured if opened), given 'window' and 'item_id' int.

    Function hover(event, window, item_id) takes in 'window', 'item_id' int and gets the image of the stall and displays
    it. winfo_width(), winfo_reqwidth(), winfo_height(), winfo_reqheight() are used to configure the position of the
    label. Grey image is shown if stall is closed, coloured image otherwise.
    """

    # Checks if stall is opened or closed and uses images accordingly
    if check_stall_opened(stall=get_stalls()[item_id], user_day=user_day, user_time=user_time):
        label_image = PhotoImage(file=image_str + get_stalls()[item_id] + image_format)
        text = ''
    else:
        label_image = PhotoImage(file=image_str + get_stalls()[item_id] + grey + image_format)
        text = 'Closed'

    # Stall Label
    stall_label_list[item_id].configure(image=label_image)
    stall_label_list[item_id].image = label_image

    # Shows 'Closed' text if stall is closed
    stall_label_list[item_id].configure(text=text, compound='center', font=font, fg='red')

    # Position the Stall Label accordingly
    x = pin_label_list[item_id].winfo_x() * 0.85 + (window.winfo_width() - map_canvas.winfo_width() - (
                stall_label_list[item_id].winfo_reqwidth() - pin_label_list[item_id].winfo_width())) * 0.68,
    y = pin_label_list[item_id].winfo_y() + (window.winfo_height() - map_canvas.winfo_height()) * 0.57
    stall_label_list[item_id].place(x=x, y=y)


# Done by Venkat
def leave(event):
    """When mouse leaves label, remove the image.

    Function leave(event) removes the image when the mouse leaves label.
    """

    # Removes all images and hide the label
    for j in range(get_number_of_stalls()):
        stall_label_list[j].image = None
        stall_label_list[j].place_forget()


# Done by Venkat
def move(event, window, clock_id):
    """When the windows resize, item of int 'clock_id' is moved accordingly given 'window'.

    Function move(event, window, item_id) positions the clock to the top right corner, given 'window' and int 'clock_id'
    of the clock when window resize. This allows the GUI to look proper even when resized.
    """

    # Moves the top right clock accordingly
    background_canvas.coords(clock_id, window.winfo_width() - 100, 50)

    # Check whether selected time is displayed already, and move if it is
    if time_id is not None:
        background_canvas.coords(time_id, window.winfo_width() / 2, 50)


# Done by Jun Hong
def update_time_label(clock_id):
    """Updates time accordingly, given 'clock_id' int.

    Function update_time_label(clock_id) positions the clock to the top right corner, given int 'clock_id'
    of the clock.
    """

    # Set update period
    period = 200

    # Update time label every
    background_canvas.itemconfig(tagOrId=clock_id, text=get_current_date() + '\n' + get_current_time_in_seconds())
    background_canvas.after(ms=period, func=lambda item_id=clock_id: update_time_label(clock_id=clock_id))


# Run the main program
initialize(window=GUI)
GUI.mainloop()
