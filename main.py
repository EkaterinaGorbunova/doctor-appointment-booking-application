import tkinter as tk
from tkinter import ttk

import cx_Oracle

dsn = cx_Oracle.makedsn(
    '192.168.1.231',
    '1521',
    service_name='XE'
)
conn = cx_Oracle.connect(
    user='system',
    password='system',
    dsn=dsn
)


# create execute function for quick access to it and code minimization
def oracle_execute(statement):

    c = conn.cursor()
    c.execute(statement)
    result = c.fetchall()

    c.close()

    return result

# create execute commit function to insert (update) data to database
def oracle_execute_insert(statement):

    c = conn.cursor()
    c.execute(statement)
    conn.commit()

    c.close()

# create popup window when new user is successfully created
def create_info_window(header, message):
    info_window = tk.Toplevel(main_window)
    info_window.configure(background="green")

    info_window.title(header)

    info_window_label = tk.Label(master=info_window, text=message, width=40)
    info_window_label.grid(row=0, column=0)

    info_window_button = tk.Button(master=info_window, text="OK", command=lambda: [info_window.destroy(), sign_up_window.destroy()])
    info_window_button.grid(row=1, column=0)

    info_window.mainloop()


# create popup error window when something is incorrect (username/password)
def create_error_window(header, message):
    error_window = tk.Toplevel(main_window)
    error_window.configure(background="#FF8786")

    error_window.title(header)

    error_window_label = tk.Label(master=error_window, text=message, width=60)
    error_window_label.grid(row=0, column=0)

    error_window_button = tk.Button(master=error_window, text="OK", command=lambda: error_window.destroy())
    error_window_button.grid(row=1, column=0)

    error_window.mainloop()


# check username and password input from the user input during the login step
def check_username_and_password():
    entered_username = main_window_username_entry_text.get()  # initialize a variable entered_username and assign it the value username from the user input
    entered_password = main_window_password_entry_text.get()  # initialize a variable entered_password and assign it the value password from the user input
    db_request = oracle_execute("select * from patient where username='{}'".format(entered_username))  # searching for existing DB entrie with this username (primary key). If username exists - DB will return all attributes (columns), including password
    if len(db_request) == 0:  # if entered username does not exist in table - DB will return an empty list
        create_error_window("ERROR", "Entered user does not exist. Please, correct entered username or register!")  # display popup error message
    elif len(entered_password.strip()) == 0:  # if user did not write the password; strip deletes extra spaces at the beginning and at the end
        create_error_window("ERROR", "You have entered empty password!")  # display popup error message
    elif entered_password.strip() != db_request[0][1]:  # check if the password entered from the user does not equal the password stored in db; where [0] - idnetifies the list containing all attributes of this patient and [1] identifies an index of the password in the list of attributes of patient
        create_error_window("ERROR", "You have entered incorrect password!")  # display popup error message if passwords not equal
    elif entered_password.strip() == db_request[0][1]:  # check if the password entered by user equels password in DB
        book_an_appointment_window()

# check if username entered during registration already exists in db, or is empty. + check if password is empty
def validate_usermame_password_during_registration (entered_username, entered_password):
    validation_passed = True
    db_request = oracle_execute("select * from patient where username='{}'".format(entered_username))

    if entered_username == "":
        sign_up_window_username_entry.configure(bg='#FF8786')
        sign_up_window_username_entry_text.set("USERNAME CAN NOT BE EMPTY")
        validation_passed = False

    elif len(db_request) == 1: # if length of the list returned from db equels 1 - it means user with same username already exists in the db
        sign_up_window_username_entry.configure(bg='#FF8786')
        sign_up_window_username_entry_text.set("USERNAME ALREADY EXISTS")
        validation_passed = False

    if entered_password == "":
        sign_up_window_password_entry.configure(bg='#FF8786')
        sign_up_window_password_entry_text.set("PASSWORD CAN NOT BE EMPTY")
        validation_passed = False

    return validation_passed

def create_sign_up_window():
    global sign_up_window
    sign_up_window = tk.Toplevel(main_window)
    sign_up_window.configure(background="light blue")
    sign_up_window.title("Doctor's Appointment App")

    # create main Frame
    Frame = tk.Frame(master=sign_up_window, relief=tk.RAISED, borderwidth=frameBorderWidth)
    Frame.grid(row=1, column=0, padx=padx, pady=pady, columnspan=2, sticky='w')

    # create label "Creating a new account"
    sign_up_window_new_accountlabel = tk.Label(master=sign_up_window, text="Creating a new account",
                                               background="light blue", font="Helvetica 12 bold")
    sign_up_window_new_accountlabel.grid(row=0, column=0, padx=padx, pady=pady, sticky="w")

    # create the First Name field
    sign_up_window_first_name_label = tk.Label(master=Frame, text="First Name", font="Helvetica 10")
    sign_up_window_first_name_label.grid(row=1, column=0, padx=padx, pady=pady, sticky="w")

    global sign_up_window_first_name_entry_text
    sign_up_window_first_name_entry_text = tk.StringVar()
    sign_up_window_first_name_entry = tk.Entry(master=Frame, textvariable=sign_up_window_first_name_entry_text,
                                               width=30)
    sign_up_window_first_name_entry.grid(row=1, column=1)

    # create the Last Name field
    sign_up_window_last_name_label = tk.Label(master=Frame, text="Last Name", font="Helvetica 10")
    sign_up_window_last_name_label.grid(row=2, column=0, padx=padx, pady=pady, sticky="w")

    global sign_up_window_last_name_entry_text
    sign_up_window_last_name_entry_text = tk.StringVar()
    sign_up_window_last_name_entry = tk.Entry(master=Frame, textvariable=sign_up_window_last_name_entry_text, width=30)
    sign_up_window_last_name_entry.grid(row=2, column=1)

    # create Gender field
    sign_up_window_gender_label = tk.Label(master=Frame, text="Gender", font="Helvetica 10")
    sign_up_window_gender_label.grid(row=3, column=0, padx=padx, pady=pady, sticky="w")

    # gender variable
    global sign_up_window_gender
    sign_up_window_gender = tk.StringVar()
    sign_up_window_gender.set('M')

    # create two radio buttons
    male = tk.Radiobutton(master=Frame, text="Male", variable=sign_up_window_gender, value='M', font="Helvetica 10")
    male.grid(row=3, column=1, sticky="w")

    female = tk.Radiobutton(master=Frame, text="Female", variable=sign_up_window_gender, value='F', font="Helvetica 10")
    female.grid(row=4, column=1, sticky="w")

    # create city field
    sign_up_window_city_label = tk.Label(master=Frame, text="City", font="Helvetica 10")
    sign_up_window_city_label.grid(row=5, column=0, padx=padx, pady=pady, sticky="w")

    global sign_up_window_city_entry_text
    sign_up_window_city_entry_text = tk.StringVar()
    sign_up_window_city_entry = tk.Entry(master=Frame, textvariable=sign_up_window_city_entry_text, width=30)
    sign_up_window_city_entry.grid(row=5, column=1)

    # create address field
    sign_up_window_address_label = tk.Label(master=Frame, text="Address", font="Helvetica 10")
    sign_up_window_address_label.grid(row=6, column=0, padx=padx, pady=pady, sticky="w")

    global sign_up_window_address_entry_text
    sign_up_window_address_entry_text = tk.StringVar()
    sign_up_window_address_entry = tk.Entry(master=Frame, textvariable=sign_up_window_address_entry_text, width=30)
    sign_up_window_address_entry.grid(row=6, column=1)

    # create username field
    sign_up_window_username_label = tk.Label(master=Frame, text="Username", font="Helvetica 10")
    sign_up_window_username_label.grid(row=7, column=0, padx=padx, pady=pady, sticky="w")

    global sign_up_window_username_entry_text
    sign_up_window_username_entry_text = tk.StringVar()
    global sign_up_window_username_entry
    sign_up_window_username_entry = tk.Entry(master=Frame, textvariable=sign_up_window_username_entry_text, width=30)
    sign_up_window_username_entry.grid(row=7, column=1)

    # create password field
    main_window_password_label = tk.Label(master=Frame, text="Password:", font="Helvetica 10")
    main_window_password_label.grid(row=8, column=0, padx=padx, pady=pady, sticky="w")

    global sign_up_window_password_entry_text
    sign_up_window_password_entry_text = tk.StringVar()
    global sign_up_window_password_entry
    sign_up_window_password_entry = tk.Entry(master=Frame, textvariable=sign_up_window_password_entry_text, width=30)
    sign_up_window_password_entry.grid(row=8, column=1, padx=padx, pady=pady, sticky="w")

    # create button Frame
    Frame_buttons = tk.Frame(master=sign_up_window, background="light blue")
    Frame_buttons.grid(row=2, column=0, padx=padx, pady=pady, columnspan=3)

    sign_up_window_button = tk.Button(master=Frame_buttons, text="Register", command=adding_user_to_db)
    sign_up_window_button.grid(row=0, column=0, padx=5, pady=5)

    sign_up_window_button_clear = tk.Button(master=Frame_buttons, text="Clear",
                                            command=lambda: [sign_up_window_first_name_entry_text.set(""),
                                                             sign_up_window_last_name_entry_text.set(""),
                                                             sign_up_window_gender.set("M"),
                                                             sign_up_window_city_entry_text.set(""),
                                                             sign_up_window_address_entry_text.set(""),
                                                             sign_up_window_username_entry_text.set(""),
                                                             sign_up_window_username_entry.configure(bg='white'),
                                                             sign_up_window_password_entry_text.set(""),
                                                             sign_up_window_password_entry.configure(bg='white')])
    sign_up_window_button_clear.grid(row=0, column=1, padx=5, pady=5)

    sign_up_window_button_cancel = tk.Button(master=Frame_buttons, text="Cancel", command=lambda: sign_up_window.destroy())
    sign_up_window_button_cancel.grid(row=0, column=2, padx=5, pady=5)

    sign_up_window.mainloop()


def adding_user_to_db():
    entered_first_name = sign_up_window_first_name_entry_text.get()
    entered_last_name = sign_up_window_last_name_entry_text.get()
    entered_gender = sign_up_window_gender.get()
    entered_city = sign_up_window_city_entry_text.get()
    entered_address = sign_up_window_address_entry_text.get()
    entered_username = sign_up_window_username_entry_text.get()
    entered_password = sign_up_window_password_entry_text.get()

    # if validation of the username and password was True - add new user to the patient table
    if validate_usermame_password_during_registration(entered_username, entered_password):
        db_request = oracle_execute_insert(
            "insert into patient (first_name, last_name, gender, city, address, username, password) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                entered_first_name, entered_last_name, entered_gender, entered_city, entered_address, entered_username,
                entered_password))
        db_request = oracle_execute("select * from patient where username='{}'".format(entered_username))
        if len(db_request) != 0:
            create_info_window("INFO", "You have successfully registered!")  # if the user successfully is added to display popup info message



def book_an_appointment_window():
    book_an_appointment_window = tk.Toplevel(main_window)
    book_an_appointment_window.configure(background="light blue")
    book_an_appointment_window.title("Doctor's Appointment App")

    global username
    username = main_window_username_entry_text.get()

    Frame_username = tk.Frame(master=book_an_appointment_window, background="light blue")
    Frame_username.grid(row=0, column=0, padx=padx, pady=pady, columnspan=2)

    # create the username field
    book_an_appointment_window_username = tk.Label(master=Frame_username, text="Username: {}".format(username), font="Helvetica 12 bold", background="light blue")
    book_an_appointment_window_username.grid(row=0, column=0)

    # create main Frame
    Frame_userinfo = tk.Frame(master=book_an_appointment_window, relief=tk.RAISED, borderwidth=frameBorderWidth)
    Frame_userinfo.grid(row=1, column=0, padx=padx, pady=pady, sticky="n")

    # read user info from db to fill current user informtion fields
    db_request = oracle_execute("select * from patient where username='{}'".format(username))

    book_an_appointment_window_first_name_label = tk.Label(master=Frame_userinfo, text="First Name:", font="Helvetica 10 bold")
    book_an_appointment_window_first_name_label.grid(row=0, column=0, padx=padx, pady=pady, sticky='w')

    book_an_appointment_window_first_name_value = tk.Label(master=Frame_userinfo, text="{}".format(db_request[0][2]))
    book_an_appointment_window_first_name_value.grid(row=0, column=1, padx=padx, pady=pady, sticky='w')

    book_an_appointment_window_last_name_label = tk.Label(master=Frame_userinfo, text="Last Name:", font="Helvetica 10 bold")
    book_an_appointment_window_last_name_label.grid(row=1, column=0, padx=padx, pady=pady, sticky='w')

    book_an_appointment_window_last_name_value = tk.Label(master=Frame_userinfo, text="{}".format(db_request[0][3]))
    book_an_appointment_window_last_name_value.grid(row=1, column=1, padx=padx, pady=pady, sticky='w')

    book_an_appointment_window_gender_label = tk.Label(master=Frame_userinfo, text="Gender:", font="Helvetica 10 bold")
    book_an_appointment_window_gender_label.grid(row=2, column=0, padx=padx, pady=pady, sticky='w')

    book_an_appointment_window_gender_value = tk.Label(master=Frame_userinfo, text="{}".format(db_request[0][4]))
    book_an_appointment_window_gender_value.grid(row=2, column=1, padx=padx, pady=pady, sticky='w')

    book_an_appointment_window_city_label = tk.Label(master=Frame_userinfo, text="City:", font="Helvetica 10 bold")
    book_an_appointment_window_city_label.grid(row=0, column=2, padx=padx, pady=pady, sticky='w')

    book_an_appointment_window_city_value = tk.Label(master=Frame_userinfo, text="{}".format(db_request[0][5]))
    book_an_appointment_window_city_value.grid(row=0, column=3, padx=padx, pady=pady, sticky='w')

    book_an_appointment_window_address_label = tk.Label(master=Frame_userinfo, text="Address:", font="Helvetica 10 bold")
    book_an_appointment_window_address_label.grid(row=1, column=2, padx=padx, pady=pady, sticky='w')

    book_an_appointment_window_address_value = tk.Label(master=Frame_userinfo, text="{}".format(db_request[0][6]))
    book_an_appointment_window_address_value.grid(row=1, column=3, padx=padx, pady=pady, sticky='w')

    current_scheduled_appointments_label = tk.Label(master=Frame_userinfo, text="Your scheduled appointment:", font="Helvetica 10 bold")
    current_scheduled_appointments_label.grid(row=3, column=0, padx=padx, pady=pady, sticky="w", columnspan=4)

    # variable to show next appointment (time) reserved by this user
    global next_scheduled_appointment_lable_text
    next_scheduled_appointment_lable_text = tk.StringVar()
    next_scheduled_appointment_label = tk.Label(master=Frame_userinfo, textvariable=next_scheduled_appointment_lable_text)
    next_scheduled_appointment_label.grid(row=4, column=0, padx=padx, pady=pady, sticky="w")

    # run db request to find lines in appointment table where this user is in username column. TO_CHAR converts Date format into String
    db_request_existing_appointments = oracle_execute("SELECT TO_CHAR(appointment_date, 'DD-MON-YYYY HH24:MI:SS') from appointment where username='{}'".format(username))

    # check if user have any lines reserved (to avoid trying to read index 0 from the empty list)
    if len(db_request_existing_appointments) != 0:
        next_scheduled_appointment_lable_text.set(db_request_existing_appointments[0][0]) # if user have existing appointment - take Date value and assign to info Label

    Frame_booking_info = tk.Frame(master=book_an_appointment_window, relief=tk.RAISED, borderwidth=frameBorderWidth)
    Frame_booking_info.grid(row=1, column=1, padx=padx, pady=pady, sticky="n")

    book_an_appointment_window_booking_label = tk.Label(master=Frame_booking_info, text="Book an Appointment", font="Helvetica 12 bold")
    book_an_appointment_window_booking_label.grid(row=0, column=0, padx=padx, pady=pady, columnspan=2)

    book_an_appointment_window_doctor_name_value = tk.Label(master=Frame_booking_info, text="Doctor:", font="Helvetica 10 bold")
    book_an_appointment_window_doctor_name_value.grid(row=1, column=0, padx=padx, pady=pady, sticky='w')

    global book_an_appointment_window_doctor_name_optionmenu_value
    book_an_appointment_window_doctor_name_optionmenu_value = tk.StringVar()
    book_an_appointment_window_doctor_name_optionmenu_value.set("Andy") # Set default value of the drop-down list. It must be part of element's values.
    # use Comboblox widgit to create drop-down menu
    book_an_appointment_window_doctor_name_optionmenu = ttk.Combobox(Frame_booking_info, textvariable=book_an_appointment_window_doctor_name_optionmenu_value, values=["Andy", "Charlie"])
    book_an_appointment_window_doctor_name_optionmenu.grid(row=1, column=1, padx=padx, pady=pady, sticky='w')

    book_an_appointment_window_day_value = tk.Label(master=Frame_booking_info, text="Day:",
                                                            font="Helvetica 10 bold")
    book_an_appointment_window_day_value.grid(row=2, column=0, padx=padx, pady=pady, sticky='w')

    global book_an_appointment_window_day_optionmenu_value
    book_an_appointment_window_day_optionmenu_value = tk.StringVar()
    book_an_appointment_window_day_optionmenu_value.set("01")
    book_an_appointment_window_day_optionmenu = ttk.Combobox(Frame_booking_info,
                                                                      textvariable=book_an_appointment_window_day_optionmenu_value,
                                                                      values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"])
    book_an_appointment_window_day_optionmenu.grid(row=2, column=1, padx=padx, pady=pady, sticky='w')


    book_an_appointment_window_month_value = tk.Label(master=Frame_booking_info, text="Month:", font="Helvetica 10 bold")
    book_an_appointment_window_month_value.grid(row=3, column=0, padx=padx, pady=pady, sticky='w')

    global book_an_appointment_window_month_optionmenu_value
    book_an_appointment_window_month_optionmenu_value = tk.StringVar()
    book_an_appointment_window_month_optionmenu_value.set("JAN")
    book_an_appointment_window_month_optionmenu = ttk.Combobox(Frame_booking_info,
                                                                      textvariable=book_an_appointment_window_month_optionmenu_value,
                                                                      values=["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"])
    book_an_appointment_window_month_optionmenu.grid(row=3, column=1, padx=padx, pady=pady, sticky='w')


    book_an_appointment_window_year_value = tk.Label(master=Frame_booking_info, text="Year:", font="Helvetica 10 bold")
    book_an_appointment_window_year_value.grid(row=4, column=0, padx=padx, pady=pady, sticky='w')

    global book_an_appointment_window_year_optionmenu_value
    book_an_appointment_window_year_optionmenu_value = tk.StringVar()
    book_an_appointment_window_year_optionmenu_value.set("2020")
    book_an_appointment_window_year_optionmenu = ttk.Combobox(Frame_booking_info, textvariable=book_an_appointment_window_year_optionmenu_value,
                                                                      values=["2020", "2021", "2022"], state="readonly")
    book_an_appointment_window_year_optionmenu.grid(row=4, column=1, padx=padx, pady=pady, sticky='w')

    book_an_appointment_optionmenu_button = tk.Button(master=Frame_booking_info, text="Search", command=search_available_appointments)
    book_an_appointment_optionmenu_button.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

# function to find in table appointment all lines where username is empty
def search_available_appointments():
    selected_doctor = book_an_appointment_window_doctor_name_optionmenu_value.get()
    # form a string to use in SQL request. Concatenate/merge day, month and year variables that user entered. Need to convert to String before.
    selected_date = str(book_an_appointment_window_day_optionmenu_value.get()) + "-" + str(
        book_an_appointment_window_month_optionmenu_value.get()) + "-" + str(
        book_an_appointment_window_year_optionmenu_value.get())

    # variable (list) will contain appointment_dates for lines where date and doctor_name equel user input
    global available_appointments
    available_appointments = oracle_execute(
        "SELECT TO_CHAR(appointment_date, 'DD-MON-YYYY HH24:MI:SS') FROM appointment WHERE doctor_name = '{}' AND (appointment_date > TO_DATE('{} 00:00:00', 'DD-MONTH-YYYY HH24:MI:SS') AND appointment_date < TO_DATE('{} 23:59:59', 'DD-MONTH-YYYY HH24:MI:SS'))".format(
            selected_doctor, selected_date, selected_date))

    # send list of available times (for this doctor) to next function
    display_appointment_search_results(available_appointments)

    return True

def display_appointment_search_results(available_appointments):

    make_new_appointment_window = tk.Toplevel(main_window)
    make_new_appointment_window.configure(background="light blue")
    make_new_appointment_window.title("Book new appointment")

    ## Frame containing appoinment search results
    Frame_available_appointments = tk.Frame(master=make_new_appointment_window, relief=tk.RAISED, borderwidth=frameBorderWidth)
    Frame_available_appointments.grid(row=0, column=0, padx=padx, pady=pady)

    if len(available_appointments) != 0:

        # selected appointment (to book) variable
        global selected_appointment_to_book
        selected_appointment_to_book = tk.StringVar()
        selected_appointment_to_book.set(available_appointments[0][0])

        i = 0  # fills line by line
        for available_appointment in available_appointments:
            # create radio button for every index in returned list of available appointments
            radio_button = tk.Radiobutton(master=Frame_available_appointments, text=available_appointment[0], variable=selected_appointment_to_book, value=available_appointment[0])
            radio_button.grid(row=i, column=0, sticky="w")
            i = i + 1

        ## Frame containing appoinment search results
        Frame_book_appointment = tk.Frame(master=make_new_appointment_window, background="light blue")
        Frame_book_appointment.grid(row=1, column=0, padx=padx, pady=pady)

        book_an_appointment_button = tk.Button(master=Frame_book_appointment, text="Book", command=lambda:[next_scheduled_appointment_lable_text.set(selected_appointment_to_book.get()), make_new_appointment_window.destroy(), oracle_execute_insert("UPDATE appointment SET username = '{}' WHERE appointment_date = TO_DATE('{}', 'DD-MON-YYYY HH24:MI:SS')".format(username, selected_appointment_to_book.get()))])
        book_an_appointment_button.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

    return True

    book_an_appointment_window.mainloop()


main_window = tk.Tk()
main_window.configure(background="light blue")
main_window.title("Doctor's Appointment App")

frameBorderWidth = 3
padx = 5
pady = 5

# create label "Login"
main_window_login = tk.Label(master=main_window, text="Login",
                             background="light blue", font="Helvetica 12 bold")
main_window_login.grid(row=1, column=0, padx=padx, sticky='w')

Frame = tk.Frame(master=main_window, relief=tk.RAISED, borderwidth=frameBorderWidth)
Frame.grid(row=2, column=0, padx=padx, pady=pady, columnspan=2, sticky='w')

# create username field
main_window_username_label = tk.Label(master=Frame, text="Username:", font="Helvetica 10")
main_window_username_label.grid(row=0, column=0, padx=padx, pady=pady)

main_window_username_entry_text = tk.StringVar()
main_window_username_entry = tk.Entry(master=Frame, textvariable=main_window_username_entry_text, width=20)
main_window_username_entry.grid(row=0, column=1, padx=padx, pady=pady)

# create password field
main_window_password_label = tk.Label(master=Frame, text="Password:", font="Helvetica 10")
main_window_password_label.grid(row=1, column=0, padx=padx, pady=pady)

main_window_password_entry_text = tk.StringVar()
main_window_password_entry = tk.Entry(master=Frame, show="*", textvariable=main_window_password_entry_text,
                                      width=20)
main_window_password_entry.grid(row=1, column=1, padx=padx, pady=pady)

# create button Frame
Frame_main_buttons = tk.Frame(master=main_window, background="light blue")
Frame_main_buttons.grid(row=4, column=0, padx=padx, pady=pady, columnspan=2)

# create login field
main_window_button_login = tk.Button(master=Frame_main_buttons, text="Login", command=check_username_and_password)
main_window_button_login.grid(row=0, column=0, padx=5, pady=0)

main_window_button_signup = tk.Button(master=Frame_main_buttons, text="Sign up", command=create_sign_up_window)
main_window_button_signup.grid(row=0, column=1, padx=5, pady=5)

# create button clear
main_window_button_clear = tk.Button(master=Frame_main_buttons, text="Clear",
                                     command=lambda: [main_window_username_entry_text.set(""),
                                                      main_window_password_entry_text.set("")])

main_window_button_clear.grid(row=0, column=2, padx=0, pady=5)

main_window.mainloop()

conn.close()
