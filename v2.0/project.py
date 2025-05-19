import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore
from datetime import datetime, timezone
import os
import csv
import bcrypt
import sys


# Define file paths as constants
PATH = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(PATH, "icon.ico")
DB_PATH = os.path.join(PATH, "study_tracker.db")


# Creating the app object
app = QtWidgets.QApplication(sys.argv)


# Creating the window objects
main_window = QtWidgets.QWidget()
reg_window = QtWidgets.QWidget()
login_window = QtWidgets.QWidget()
user_window = QtWidgets.QWidget()
session_window = QtWidgets.QWidget()
stats_window = QtWidgets.QWidget()


def main():
    # Creating the database
    create_database()

    ## Formatting the main window
    # Adjusting the main window layout
    adjust_window(main_window)

    # Creating a a main label
    main_label = QtWidgets.QLabel("Welcome to Study Tracker v2.0!", main_window)
    main_label.move(55, 50)
    main_label.setStyleSheet("font-weight: bold; font-size: 12pt;")

    # Creating a register button
    main_reg_btn = QtWidgets.QPushButton("Register", main_window)
    main_reg_btn.resize(150, 50)
    main_reg_btn.move(180, 120)
    main_reg_btn.setStyleSheet("font-size: 12pt;")
    main_reg_btn.clicked.connect(main_window.close)
    main_reg_btn.clicked.connect(register_menu)

    # Creating a log in button
    main_login_btn = QtWidgets.QPushButton("Log in", main_window)
    main_login_btn.resize(150, 50)
    main_login_btn.move(180, 180)
    main_login_btn.setStyleSheet("font-size: 12pt;")
    main_login_btn.clicked.connect(login_menu)

    # Creating an exit button
    main_exit_btn = QtWidgets.QPushButton("Exit", main_window)
    main_exit_btn.resize(150, 50)
    main_exit_btn.move(180, 240)
    main_exit_btn.setStyleSheet("font-size: 12pt;")
    main_exit_btn.clicked.connect(QtWidgets.QApplication.quit)

    ## Formatting the register window
    # Adjusting the register window layout
    adjust_window(reg_window)

    # Creating a username label
    username_label = QtWidgets.QLabel("Username", reg_window)
    username_label.move(30, 35)
    username_label.setStyleSheet("font-size: 10pt;")

    # Creating a username input field
    reg_username_input = QtWidgets.QLineEdit(reg_window)
    reg_username_input.move(220, 35)
    reg_username_input.resize(230, 30)
    reg_username_input.setStyleSheet("font-size: 10pt;")
    reg_username_input.setPlaceholderText("Choose a username")

    # Creating a password label
    pw_label = QtWidgets.QLabel("Password", reg_window)
    pw_label.move(30, 85)
    pw_label.setStyleSheet("font-size: 10pt;")

    # Creating a password input field
    reg_pw_input = QtWidgets.QLineEdit(reg_window)
    reg_pw_input.setEchoMode(QtWidgets.QLineEdit.Password)
    reg_pw_input.move(220, 85)
    reg_pw_input.resize(230, 30)
    reg_pw_input.setStyleSheet("font-size: 10pt;")
    reg_pw_input.setPlaceholderText("Choose a password")

    # Creating a confirm password label
    pw_confirm_label = QtWidgets.QLabel("Confirm Password", reg_window)
    pw_confirm_label.move(30, 135)
    pw_confirm_label.setStyleSheet("font-size: 10pt;")

    # Creating a confirm password input field
    pw_confirm_input = QtWidgets.QLineEdit(reg_window)
    pw_confirm_input.setEchoMode(QtWidgets.QLineEdit.Password)
    pw_confirm_input.move(220, 135)
    pw_confirm_input.resize(230, 30)
    pw_confirm_input.setStyleSheet("font-size: 10pt;")
    pw_confirm_input.setPlaceholderText("Re-Enter your password")

    # Creating a register button
    reg_btn = QtWidgets.QPushButton("Register", reg_window)
    reg_btn.resize(150, 50)
    reg_btn.move(180, 195)
    reg_btn.setStyleSheet("font-size: 12pt;")
    reg_btn.clicked.connect(lambda: register_user(reg_username_input, reg_pw_input, pw_confirm_input))

    # Creating an return button
    reg_return_btn = QtWidgets.QPushButton("Return", reg_window)
    reg_return_btn.resize(150, 50)
    reg_return_btn.move(180, 255)
    reg_return_btn.setStyleSheet("font-size: 12pt;")
    reg_return_btn.clicked.connect(reg_window.close)
    reg_return_btn.clicked.connect(lambda: main_menu(reg_window))

    ## Formatting the log in window
    # Adjusting the log in window layout
    adjust_window(login_window)

    # Creating a username label
    username_label = QtWidgets.QLabel("Username", login_window)
    username_label.move(30, 70)
    username_label.setStyleSheet("font-size: 10pt;")

    # Creating a username input field
    username_input = QtWidgets.QLineEdit(login_window)
    username_input.move(220, 70)
    username_input.resize(230, 30)
    username_input.setStyleSheet("font-size: 10pt;")
    username_input.setPlaceholderText("Choose a username")

    # Creating a password label
    pw_label = QtWidgets.QLabel("Password", login_window)
    pw_label.move(30, 120)
    pw_label.setStyleSheet("font-size: 10pt;")

    # Creating a password input field
    pw_input = QtWidgets.QLineEdit(login_window)
    pw_input.setEchoMode(QtWidgets.QLineEdit.Password)
    pw_input.move(220, 120)
    pw_input.resize(230, 30)
    pw_input.setStyleSheet("font-size: 10pt;")
    pw_input.setPlaceholderText("Choose a password")

    # Creating a log in button
    login_btn = QtWidgets.QPushButton("Log in", login_window)
    login_btn.resize(150, 50)
    login_btn.move(180, 195)
    login_btn.setStyleSheet("font-size: 12pt;")
    login_btn.clicked.connect(lambda: login_user(username_input, pw_input))

    # Creating an return button
    login_return_btn = QtWidgets.QPushButton("Return", login_window)
    login_return_btn.resize(150, 50)
    login_return_btn.move(180, 255)
    login_return_btn.setStyleSheet("font-size: 12pt;")
    login_return_btn.clicked.connect(lambda: main_menu(login_window))

    ## Formatting the user window
    # Adjusting the user window layout
    adjust_window(user_window)

    # Creating a greeting label
    main_label = QtWidgets.QLabel("Welcome to Study Tracker v2.0!", user_window)
    main_label.move(55, 30)
    main_label.setStyleSheet("font-weight: bold; font-size: 12pt;")

    # Creating a start session button
    session_btn = QtWidgets.QPushButton("Start new session", user_window)
    session_btn.resize(250, 50)
    session_btn.move(130, 100)
    session_btn.setStyleSheet("font-size: 12pt;")
    session_btn.clicked.connect(start_session)

    # Creating a stats button
    stats_btn = QtWidgets.QPushButton("View stats", user_window)
    stats_btn.resize(250, 50)
    stats_btn.move(130, 150)
    stats_btn.setStyleSheet("font-size: 12pt;")
    stats_btn.clicked.connect(view_stats)

    # Creating a delete account button
    acc_del_btn = QtWidgets.QPushButton("Delete account", user_window)
    acc_del_btn.resize(250, 50)
    acc_del_btn.move(130, 200)
    acc_del_btn.setStyleSheet("font-size: 12pt;")
    acc_del_btn.clicked.connect(delete_account)

    # Creating an log out button
    logout_btn = QtWidgets.QPushButton("Log out", user_window)
    logout_btn.resize(250, 50)
    logout_btn.move(130, 250)
    logout_btn.setStyleSheet("font-size: 12pt;")
    logout_btn.clicked.connect(logout)

    ## Formatting the session window
    # Adjusting the session window layout
    adjust_window(session_window)

    # Handle close event for session window
    session_window.eventFilter = session_close_event
    session_window.installEventFilter(session_window)

    ## Formatting the stats window
    # Adjusting the stats window layout
    adjust_window(stats_window)

    # Adding a return button to the stats window
    stats_return_btn = QtWidgets.QPushButton("Return", stats_window)
    stats_return_btn.resize(150, 50)
    stats_return_btn.move(180, 255)
    stats_return_btn.setStyleSheet("font-size: 12pt;")
    stats_return_btn.clicked.connect(stats_return)


# Creating a function to adjust the windows
def adjust_window(window):
    window.setFixedSize(500, 350)
    window.setWindowFlags(window.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
    window.move(750, 300)
    window.setWindowIcon(QtGui.QIcon(ICON_PATH))
    window.setWindowTitle("Study Tracker")


def register_menu(): # Go to register window from main window
    main_window.close()
    reg_window.show()


def main_menu(previous_window): # Return to main window
    previous_window.close()
    main_window.show()


def login_menu(): # Go to log in window from main window
    main_window.close()
    login_window.show()


def logout(): # Return to main window from user window
    user_window.close()
    main_window.show()


def stats_return(): # Return to user window from stats window
    stats_window.close()
    user_window.show()


def create_database():
    # Connecting to the database
    db = sqlite3.connect(DB_PATH)
    # Creating the tables
    db.execute("CREATE TABLE IF NOT EXISTS users "
               "(user_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
               "username TEXT UNIQUE NOT NULL," \
               "password TEXT UNIQUE NOT NULL," \
               "register_date TEXT DEFAULT CURRENT_TIMESTAMP)")
    
    db.execute("CREATE TABLE IF NOT EXISTS sessions "
               "(session_id INTEGER PRIMARY KEY AUTOINCREMENT," \
               "user_id INTEGER," \
               "subject TEXT NOT NULL," \
               "start_time TEXT DEFAULT CURRENT_TIMESTAMP," \
               "duration REAL," \
               "FOREIGN KEY (user_id) REFERENCES users (user_id))")
    
    # Saving and exiting
    db.commit()
    db.close()


def register_user(username_input, pw_input, pw_confirm_input):
    # Get username and password from user
    username = username_input.text()
    password = pw_input.text()
    confirm_password = pw_confirm_input.text()

    # Ensure user entered a username
    if not username.strip():
        msg = QtWidgets.QMessageBox.warning(reg_window, "Input Error", "Cannot leave username field empty!")
        return
    
    # Ensure user entered a password
    if not password.strip():
        msg = QtWidgets.QMessageBox.warning(reg_window, "Input Error", "Cannot leave password field empty!")
        return
    
    # Ensure user re-entered their password
    if not confirm_password.strip():
        msg = QtWidgets.QMessageBox.warning(reg_window, "Input Error", "Must confirm your password!")
        return

    # Confirm that the 2 passwords match
    if password != confirm_password:
        msg = QtWidgets.QMessageBox.warning(reg_window, "Input Error", "Passwords do not match!")
        return
    
    # confirm the chosen password is at least 6 characters long
    if len(password) < 6:
        msg = QtWidgets.QMessageBox.warning(reg_window, "Input Error", "Password must at least be 6 characters long!")
        return

    # Register the user
    try:
        hashed_password = hash_password(password)
        db = sqlite3.connect(DB_PATH)
        cr = db.cursor()
        cr.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                (username, hashed_password))
        msg = QtWidgets.QMessageBox.information(reg_window, "Registered", "User registered successfully!")
        db.commit()
        reg_window.close()
        main_window.show()
    # Ensure that the user does not already exist
    except sqlite3.IntegrityError:
        msg = QtWidgets.QMessageBox.warning(reg_window, "Input Error", "Username already exists!")
    # Closing the database
    finally:
        db.close()

    # CLear the input fields after every registeration
    username_input.clear()
    pw_input.clear()
    pw_confirm_input.clear()


# Hash the password for secure database storage
def hash_password(pw):
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()) 


# Compare a normal password to a hashed password
def check_hashed_password(user_pw, hashed_pw):
    return bcrypt.checkpw(user_pw.encode("utf-8"), hashed_pw)


def login_user(username_input, pw_input):
    # Get username and password from user
    username = username_input.text()
    password = pw_input.text()

    # Ensure the user entered a username
    if not username.strip():
        msg = QtWidgets.QMessageBox.warning(reg_window, "Input Error", "Cannot leave username field empty!")
        return

    # Ensure the user entered a password
    if not password.strip():
        msg = QtWidgets.QMessageBox.warning(reg_window, "Input Error", "Cannot leave password field empty!")
        return
    
    # Connecting to database
    db = sqlite3.connect(DB_PATH)
    cr = db.cursor()

    # Checking if the user exists in the database
    cr.execute("SELECT user_id, password FROM users WHERE username = ?", (username,))

    user = cr.fetchone()

    if user:
        hashed_pw = user[1]
        check = check_hashed_password(password, hashed_pw) # Check if the user entered a correct password

        if check:
            global ID
            ID = user[0] # Set user id
            login_window.close() # Close log in window
            user_window.show() # Open user window
        else:
            msg = QtWidgets.QMessageBox.warning(login_window, "Log in Error", "Incorrect password!")
    
    else:
        msg = QtWidgets.QMessageBox.warning(login_window, "Log in Error", "Username does not exist!")

    # Close the database
    db.close()

    # Clearing the input fields after each attempt
    username_input.clear()
    pw_input.clear()


def view_stats():
    # Connecting to database
    db = sqlite3.connect(DB_PATH)
    cr = db.cursor()

    try:
        # Get user data
        cr.execute("SELECT COUNT(session_id) FROM sessions WHERE user_id = ?", (ID,))
        data = cr.fetchone()
        no_of_sessions = data[0]

        cr.execute("SELECT ROUND(SUM(duration)), ROUND(AVG(duration)) FROM sessions WHERE user_id = ?", (ID,))
        data = cr.fetchone()
        total_duration = data[0]
        avg_duration = data[1]

        cr.execute("SELECT COUNT(*) FROM sessions WHERE user_id = ? AND (duration > 2 AND duration < 4)", (ID,))
        data = cr.fetchone()
        normal_study_days = data[0]

        cr.execute("SELECT COUNT(*) FROM sessions WHERE user_id = ? AND duration > 4", (ID,))
        data = cr.fetchone()
        intense_study_days = data[0]

        cr.execute("SELECT COUNT(*) FROM sessions WHERE user_id = ? AND duration < 2", (ID,))
        data = cr.fetchone()
        light_study_days = data[0]

        cr.execute("SELECT MAX(duration), subject FROM sessions WHERE user_id = ?", (ID,))
        data = cr.fetchone()
        max_duration = data[0]
        max_duration_subject = data[1]

        cr.execute("SELECT COUNT(DISTINCT(subject)) FROM sessions WHERE user_id = ?", (ID,))
        data = cr.fetchone()
        no_of_subjects = data[0]

        cr.execute("SELECT subject, SUM(duration), AVG(duration) FROM sessions WHERE user_id = ? GROUP BY subject ORDER BY SUM(duration) DESC", (ID,))
        data = cr.fetchall()
        top_subject = data[0][0]
        top_subject_duration = data[0][1]
        top_subject_avg_duration = data[0][2]
        least_subject = data[-1][0]
        least_subject_duration = data[-1][1]
        least_subject_avg_duration = data[-1][2]

        # Closing previous window
        user_window.close()

        # Show user data
        stats_list = [
            f"You had a total of: {no_of_sessions} study sessions in {no_of_subjects} subjects",
            f"Your total study duration: {round(total_duration, 2)} hours",
            f"Your average study duration: {round(avg_duration, 2)} hours",
            f"Your light study sessions (sessions less than 2 hours): {light_study_days} sessions",
            f"Your normal study sessions (sessions from 2 to 4 hours): {normal_study_days} sessions",
            f"Your intense study sessions (sessions more than 4 hours): {intense_study_days} sessions",
            f"Your longest session was a {max_duration_subject} session that lasted for {round(max_duration * 60)} minutes",
            f"Your most studied subject was {top_subject} with an average of {round(top_subject_avg_duration * 60)} minutes/session "
            f"and a total of {round(top_subject_duration * 60)} minutes",
            f"Your least studied subject was {least_subject} with an average of {round(least_subject_avg_duration * 60)} minutes/session "
            f"and a total of {round(least_subject_duration * 60)} minutes"
        ]

        ## Adding to the stats window
        # Create a scroll area
        scroll = QtWidgets.QScrollArea(stats_window)
        scroll.setGeometry(20, 20, 450, 200)

        # Create a container
        container = QtWidgets.QWidget()
        container.setLayout(QtWidgets.QVBoxLayout())

        # Filling the container
        for key, value in enumerate(stats_list):
            label = QtWidgets.QLabel(f"{key+1}- {value}")
            label.setWordWrap(True)
            label.setStyleSheet("font-size: 10pt;")
            container.layout().addWidget(label)

        # Filling the scroll
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)

        # Closing database
        db.close()

        # Opening the stats window
        stats_window.show()

        # Giving the user the option to get a csv of their data
        msg = QtWidgets.QMessageBox.question(stats_window, "Export", "Would you like to export your full study data to a csv file?")

        if msg == QtWidgets.QMessageBox.Yes:
            export_to_csv()

    except (TypeError, IndexError): # Show error if user has not yet started any study sessions
        msg = QtWidgets.QMessageBox.warning(user_window, "Error", "You have not started any study sessions yet!")


def export_to_csv():
    # Ask the user to choose where to save the csv file
    file_path, _ = QtWidgets.QFileDialog.getSaveFileName(stats_window)

    # Ensure that the user chose a file path
    if not file_path:
        return

    # Ensure that the file extension is csv
    if not file_path.endswith(".csv"):
        file_path += ".csv"

    # Connecting to database
    db = sqlite3.connect(DB_PATH)
    cr = db.cursor()

    # Getting user data
    cr.execute("SELECT * FROM sessions WHERE user_id = ?", (ID,))
    data = cr.fetchall()

    # Opening a csv file
    with open(file_path, "w", newline='') as file:
        writer = csv.writer(file)
        # Writing the file headers
        writer.writerow(["session_id", "user_id", "subject", "start_time", "duration"])
        # Writing data into the file
        writer.writerows(data)

    # Show message indicating successful export to csv
    msg = QtWidgets.QMessageBox.information(stats_window, "Success", f"CSV successfully exported to {file_path}")

    # Closing database
    db.close()


def delete_account():
    # Asking user to confirm deletion
    msg = QtWidgets.QMessageBox.question(user_window, "Deleting account", "Are you sure you want to delete this account? (This action is irreversible!)")

    if msg == QtWidgets.QMessageBox.No:
        return
    
    # Connecting to database
    db = sqlite3.connect(DB_PATH)
    cr = db.cursor()

    # Deleting user account and all associated sessions
    cr.execute("DELETE FROM users WHERE user_id = ?", (ID,))
    cr.execute("DELETE FROM sessions WHERE user_id = ?", (ID,))        

    # Saving and closing database
    db.commit()
    db.close()

    # Show message to indicate successful deletion
    msg = QtWidgets.QMessageBox.information(user_window, "Deleted", "Account has been deleted!")

    # Closing user window
    user_window.close()

    # Going back to main window
    main_window.show()


def start_session():
    # Ensure that the user wants to start the session
    msg = QtWidgets.QMessageBox.question(user_window, "Start session", "Would you like to start your session?")

    if msg == QtWidgets.QMessageBox.No:
        return
    
    # Get subject of study from user
    subject, ok = QtWidgets.QInputDialog.getText(user_window, "Subject", "What subject are you studying?")

    if not subject:
        return
    
    # Connecting to database
    db = sqlite3.connect(DB_PATH)
    cr = db.cursor()

    # Starting a new session
    cr.execute("INSERT INTO sessions (user_id, subject) VALUES (?, ?)", (ID, subject))

    # Save changes to database
    db.commit()

    # Get the session id
    global session_id
    session_id = cr.lastrowid

    # Close the database
    db.close()

    ongoing_session()


def ongoing_session():
    # Closing previous window
    user_window.close()

    # Connecting to database
    db = sqlite3.connect(DB_PATH)
    cr = db.cursor()

    # Get the session start time
    cr.execute("SELECT start_time FROM sessions WHERE session_id = ?", (session_id,))

    session = cr.fetchone()[0]

    # Close the database
    db.close()

    # Converting start time to datetime object
    start_time = datetime.strptime(session, "%Y-%m-%d %H:%M:%S")

    # Ensure that the start time is in the utc timezone
    start_time = start_time.replace(tzinfo=timezone.utc)

    # Define global variables for timer calculations
    global is_paused, pause_start, pause_end, break_time, breaks, is_active, study_round, warned
    is_paused = False
    pause_start = 0
    pause_end = 0
    break_time = 0
    breaks = 0
    is_active = True
    study_round = 1
    warned = False
    
    ## Adding to the session window
    # Creating a timer label
    time_label = QtWidgets.QLabel("00:00:00", session_window)
    time_label.move(205, 80)
    time_label.setStyleSheet("font-size: 12pt; font-weight: bold;")

    # Create a timer object
    timer = QtCore.QTimer(session_window)

    # Creating a pause button
    pause_btn = QtWidgets.QPushButton("Pause", session_window)
    pause_btn.resize(150, 50)
    pause_btn.move(180, 195)
    pause_btn.setStyleSheet("font-size: 12pt;")
    pause_btn.clicked.connect(lambda: pause_timer(timer, pause_btn))

    # Updating the timer every second
    timer.timeout.connect(lambda: update_time(time_label, start_time, timer, pause_btn))
    timer.start(1000)

    # Creating an end button
    end_btn = QtWidgets.QPushButton("End", session_window)
    end_btn.resize(150, 50)
    end_btn.move(180, 255)
    end_btn.setStyleSheet("font-size: 12pt;")
    end_btn.clicked.connect(lambda: end_session(total_study_time, session_id, break_time, breaks, timer, time_label))

    # Opening the session window
    session_window.show()


def pause_timer(timer, btn):
    global pause_start, pause_end, break_time, breaks

    # Define function behaviour based on timer status
    if timer.isActive():
        timer.stop()
        btn.setText("Resume") # Change the pause button to resume
        is_paused = True
        pause_start = datetime.now(timezone.utc)
        breaks += 1 # Calculate total number of breaks taken
    else:
        timer.start(1000)
        btn.setText("Pause") # Change the resume button back to pause
        is_paused = False
        pause_end = datetime.now(timezone.utc)
        pause_time = (pause_end - pause_start).total_seconds()
        break_time += pause_time # Calculate total break time


def update_time(label, start_time, timer, btn):
    global total_study_time

    # Stop updating the timer if it is paused
    if is_paused:
        return

    current_time = datetime.now(timezone.utc)
    elapsed_time = current_time - start_time
    total_study_time = elapsed_time.total_seconds() - break_time

    # Display time in HH:MM:SS format
    hours = int(total_study_time // 3600)
    minutes = int((total_study_time % 3600) // 60)
    seconds = int(total_study_time % 60)
    label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    # Display warnings
    warnings(total_study_time, timer, btn, label)


# Health warnings check
def warnings(total_study_time, timer, btn, label):
    global study_round, warned

    # Optional break every 50 minutes
    if total_study_time >= 50 * 60 * study_round:
        study_round += 1 # Increment the study round
        msg1 = "You have been studying now for over 50 minutes. This is Awesome!"
        msg2 = """Would you like a short break to get refreshed?
You could go drink water, do some quick stretching to avoid back pains, or talk to a friend or family member and ask how they are!"""
        alert = QtWidgets.QMessageBox.warning(session_window, "50 minute reminder", msg1)
        optional_break = QtWidgets.QMessageBox.question(session_window, "Optional break", msg2)

        if optional_break == QtWidgets.QMessageBox.Yes:
            pause_timer(timer, btn)
    
    # Burnout warning after 4 hours
    if total_study_time >= 4 * 60 * 60 and not warned:
        warned = True # Record that the user has been warned
        msg1 = """Wow...
4 Hours today, impressive!
However, you might wanna take a break or even call it a day. Too much studying can cause a burnout!"""
        msg2 = "Would you like to end the session?"

        alert = QtWidgets.QMessageBox.warning(session_window, "Burnout warning", msg1)
        optional_end = QtWidgets.QMessageBox.question(session_window, "optional session end", msg2)

        if optional_end == QtWidgets.QMessageBox.Yes:
            end_session(total_study_time, session_id, break_time, breaks, timer, label)


def end_session(total_study_time, session_id, break_time, breaks, timer, label):
    # Stopping the timer
    timer.stop()

    # Deactivating the session
    global is_active
    is_active = False

    # SHow session stats
    msg1 ="Nice work!"
    msg2 = "You have just finished your study session."
    msg3 = f"Your session time was: {round(total_study_time / 60)} minutes"
    msg4 = f"You took {breaks} breaks with a total of {round(break_time / 60)} minutes"

    msg = msg1 + "\n" + msg2 + "\n" + msg3 + "\n" + msg4

    # Show motivational messages
    if break_time >= (50 * 60):
        msg5 = "Might wanna lower your break duration next time!"
        msg6 = "Too much break time during you study session can cause distractions and loss of focus and motivation"
        add_msg = "\n" + msg5 + "\n" + msg6
        msg +=  add_msg

    if total_study_time > 4 * 60 * 60:
        msg7 = "Might wanna call it a day!"
        add_msg = "\n" + msg7
        msg +=  add_msg

    elif total_study_time > 2 * 60 * 60:
        msg7 = "Is that all for today?"
        add_msg = "\n" + msg7
        msg +=  add_msg

    elif total_study_time < 2 * 60 * 60:
        msg7 = "Waiting for you to come back for the next session!"
        add_msg = "\n" + msg7
        msg +=  add_msg
    
    # Connect to database
    db = sqlite3.connect(DB_PATH)
    cr = db.cursor()

    # Recording session duration
    cr.execute("UPDATE sessions SET duration = ? where session_id = ?", (total_study_time / 3600, session_id))

    # Saving and closing database
    db.commit()
    db.close()

    # Display the messages
    display_msg = QtWidgets.QMessageBox.about(session_window, "Session end", msg)

    # Resetting the timer
    label.setText("")

    # Closing session window
    session_window.close()

    # Going back to user window
    user_window.show()


# Disable close events while the session is ongoing
def session_close_event(obj, event):
    if event.type() == QtCore.QEvent.Close:
        if is_active:
            msg = QtWidgets.QMessageBox.warning(session_window, "Close error", "Please end the session before closing the window")
            event.ignore()
            return True
    return False


if __name__ == "__main__": # Start the program
    main() # Start main function
    main_window.show() # Show main window
    app.exec_() # Start app object