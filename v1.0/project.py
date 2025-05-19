import sqlite3
from datetime import datetime, timezone
import time
import os
import csv
import bcrypt


PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PATH, "study_tracker.db")
CSV_PATH = os.path.join(PATH, "data.csv")


def main():
    # Creating the database file
    create_database()

    # Start the main menu
    main_menu()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
    while True:
        print("Welcome to Study Tracker v1.0!")
        choice = input("1- Register\n2- Log in\n3- Exit\n")

        if choice == "1":
            clear_screen()
            register_user()
        
        elif choice == "2":
            clear_screen()
            login_user()
        
        else:
            input("Hope to see you again soon!")
            break


def create_database():
    # Connecting to the database
    db = sqlite3.connect(DB_PATH)
    # Creating the tables
    db.execute("CREATE TABLE IF NOT EXISTS users "
               "(user_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
               "username TEXT UNIQUE NOT NULL," \
               "password TEXT UNIQUE NOT NULL)")
    
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


def register_user():
    try:
        while True:
            # Get username and password from user
            username = input("Username: ")
            password = input("Password: ")
            confirm_password = input("Confirm your password: ")

            # Username confirmation
            if not username.strip():
                input("Username cannot be empty!")
                clear_screen()
                continue
            
            # Password confirmation
            if password != confirm_password:
                input("Passwords do not match!")
                clear_screen()
                continue
            
            if len(password) < 6:
                input("Password must at least be 6 characters long!")
                clear_screen()
                continue
            
            # Register the user
            try:
                hashed_password = hash_password(password)
                db = sqlite3.connect(DB_PATH)
                cr = db.cursor()
                cr.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                        (username, hashed_password))
                print("User registered successfully!")
                db.commit()
                return
            # Ensure that the user does not already exist
            except sqlite3.IntegrityError:
                print("Username already exists!")
                return
            # Closing the database
            finally:
                db.close()
        
    except KeyboardInterrupt:
        clear_screen()


def hash_password(pw):
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt())


def check_hashed_password(user_pw, hashed_pw):
    return bcrypt.checkpw(user_pw.encode("utf-8"), hashed_pw)


def login_user():
    try:
        while True:
            # Get username and password from user
            username = input("Username: ")
            password = input("Password: ")

            # Connecting to database
            db = sqlite3.connect(DB_PATH)
            cr = db.cursor()

            # Checking if the user exists in the database
            cr.execute("SELECT user_id, password FROM users WHERE username = ?", (username,))

            user = cr.fetchone()

            if user:
                hashed_pw = user[1]
                check = check_hashed_password(password, hashed_pw)

                if check:
                    id = user[0]
                    db.close()
                    clear_screen()
                    print(f"Welcome {username}!")
                    return user_menu(id)

            # Close the database
            db.close()

            input("Invalid login attempt!")
            clear_screen()

    except KeyboardInterrupt:
        clear_screen()


def user_menu(id):
    while True:
        print("Welcome to Study Tracker v1.0!")
        choice = input("1- Start a new session\n2- View stats\n3- Delete account\n4- Log out\n")

        if choice == "1":
            clear_screen()
            start_session(id)
        
        elif choice == "2":
            clear_screen()
            view_stats(id)

        elif choice == "3":
            clear_screen()
            choice = input("Are you sure you wish to delete your account? ")

            if choice.lower() in ["yes", "y"]:
                delete_account(id)
                break
        
        else:
            clear_screen()
            return


def view_stats(id):
    # Connecting to database
    db = sqlite3.connect(DB_PATH)
    cr = db.cursor()

    try:
        # Get user data
        cr.execute("SELECT COUNT(session_id) FROM sessions WHERE user_id = ?", (id,))
        data = cr.fetchone()
        no_of_sessions = data[0]

        cr.execute("SELECT ROUND(SUM(duration)), ROUND(AVG(duration)) FROM sessions WHERE user_id = ?", (id,))
        data = cr.fetchone()
        total_duration = data[0]/60
        avg_duration = data[1]/60

        cr.execute("SELECT COUNT(*) FROM sessions WHERE user_id = ? AND duration > 120", (id,))
        data = cr.fetchone()
        normal_study_days = data[0]

        cr.execute("SELECT COUNT(*) FROM sessions WHERE user_id = ? AND duration > 240", (id,))
        data = cr.fetchone()
        intense_study_days = data[0]

        cr.execute("SELECT COUNT(*) FROM sessions WHERE user_id = ? AND duration < 120", (id,))
        data = cr.fetchone()
        light_study_days = data[0]

        cr.execute("SELECT MAX(duration), subject FROM sessions WHERE user_id = ?", (id,))
        data = cr.fetchone()
        max_duration = data[0]
        max_duration_subject = data[1]

        cr.execute("SELECT COUNT(DISTINCT(subject)) FROM sessions WHERE user_id = ?", (id,))
        data = cr.fetchone()
        no_of_subjects = data[0]

        cr.execute("SELECT subject, SUM(duration), AVG(duration) FROM sessions WHERE user_id = ? GROUP BY subject ORDER BY SUM(duration) DESC", (id,))
        data = cr.fetchall()
        top_subject = data[0][0]
        top_subject_duration = data[0][1]
        top_subject_avg_duration = data[0][2]
        least_subject = data[-1][0]
        least_subject_duration = data[-1][1]
        least_subject_avg_duration = data[-1][2]

        # Printing user data
        print(f"You had a total of: {no_of_sessions} study sessions in {no_of_subjects} subjects")
        print(f"Your total study duration: {round(total_duration, 2)} hours")
        print(f"Your average study duration: {round(avg_duration, 2)} hours")
        print(f"Your light study sessions (sessions less than 2 hours): {light_study_days} sessions")
        print(f"Your normal study sessions (sessions from 2 to 4 hours): {normal_study_days} sessions")
        print(f"Your intense study sessions (sessions more than 4 hours): {intense_study_days} sessions")
        print(f"Your longest session was a {max_duration_subject} session that lasted for {round(max_duration)} minutes")
        print(f"Your most studied subject was {top_subject} with an average of {round(top_subject_avg_duration)} minutes/session and a total of {round(top_subject_duration)} minutes")
        print(f"Your least studied subject was {least_subject} with an average of {round(least_subject_avg_duration)} minutes/session and a total of {round(least_subject_duration)} minutes")

        # Closing database
        db.close()

        # Giving the user the option to get a csv of their data
        choice = input("Would you like to export your full study data to a csv file? ")

        clear_screen()

        if choice.lower() in ["yes", "y"]:
            export_to_csv(id)

    except TypeError:
        print("You have not started any study sessions yet!")


def export_to_csv(id):
    # Connecting to database
    db = sqlite3.connect(DB_PATH)
    cr = db.cursor()

    # Getting user data
    cr.execute("SELECT * FROM sessions WHERE user_id = ?", (id,))
    data = cr.fetchall()

    # Opening a csv file
    with open(CSV_PATH, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["session_id", "user_id", "subject", "start_time", "duration"])
        writer.writerows(data)

    print(f"CSV successfully exported to {CSV_PATH}")

    # Closing database
    db.close()


def delete_account(id):
    # Connecting to database
    db = sqlite3.connect(DB_PATH)
    cr = db.cursor()

    cr.execute("DELETE FROM users WHERE user_id = ?", (id,))
    cr.execute("DELETE FROM sessions WHERE user_id = ?", (id,))        

    # Saving and closing database
    db.commit()
    db.close()

    print("Account has been deleted!")
    return


def start_session(id):
    choice = input("Would you like to start your session? ")

    if choice.lower() not in ["yes", "y"]:
        return
    
    subject = input("What subject are you studying? ")

    # Connecting to database
    db = sqlite3.connect(DB_PATH)
    cr = db.cursor()

    # Starting a new session
    cr.execute("INSERT INTO sessions (user_id, subject) VALUES (?, ?)", (id, subject))

    db.commit()

    # Get the session id
    session_id = cr.lastrowid

    # Close the database
    db.close()

    ongoing_session(session_id, id)


def ongoing_session(session_id, id):

    break_time = 0
    round = 0
    duration = 0
    limit = False
    mini_break = 0
    breaks = 0

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

    try:
        # Start the timer
        while True:
            # Get the current time
            current_time = datetime.now(timezone.utc)
            # Get the duration of studying
            duration = current_time - start_time 
            duration = duration.total_seconds()

            # Get the total study time
            total_study_time = (round * 50) + (duration / 60)

            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)

            clear_screen()
            # Display timer
            print(f"Study time: {hours:02}: {minutes:02}: {seconds:02}")
            # Wait 1 second before updating the timer
            time.sleep(1)

            # Warning the user against burnout if study time exceeds 4 hours
            if limit == False and total_study_time > 4 * 60:
                print("Wow...")
                print("4 hours today, impressive!")
                print("Be mindful not to get lost in time while studying.")
                print("It would benefit no one if you get a burnout!")
                decision = input("Would you like to stop and call it a day? ")
                
                if decision.lower() in ["yes", "y"]:
                    print("Great decision!")
                    return end_session(total_study_time, session_id, id)
                else:
                    input("I love your spirit! Just make sure you are balancing studying with other activities in your life, like sports and socialising!")
                    limit = True

            # Give the user an option to take a quick break every 50 minutes
            if duration >= ((mini_break + 1) * 50 * 60):
                print("You have successfully completed 50 minutes of studying!")
                print("To avoid any negative effects, it is recommended that you take a short break!")
                print("The break is to get some water, move your body and maybe talk to a friend or a family member and ask them how they are doing!")
                print("Note that this break is optional and depends on your preferences we just thought to remind you not to lose sense of time while studying!")
                user_choice = input("Take the break? ")
                mini_break += 1

                if user_choice.lower() in ["yes", "y"]:
                    break_start = datetime.now(timezone.utc)
                    input("Press any key to continue with your session...")
                    break_end = datetime.now(timezone.utc)
                    break_time += (break_end - break_start).total_seconds()
                    breaks += 1
                    mini_break = 0
                    round += 1
                    start_time = datetime.now(timezone.utc)
    
    except KeyboardInterrupt:
        clear_screen()
        print("You have ended the session!")
        end_session(total_study_time, session_id, id, break_time, breaks)


def end_session(total_study_time, session_id, id, break_time, breaks):
    # Print total study time
    print("Nice work!")
    print("You have just finished your study session.")
    print(f"Your session time was: {round(total_study_time)} minutes")
    print(f"You took {breaks} breaks with a total of {round(break_time / 60)} minutes")

    if break_time >= (50 * 60):
        print("Might wanna lower your break duration next time!")
        print("Too much break time during you study session can cause distractions and loss of focus and motivation")

    if total_study_time > 4 * 60:
        print("Might wanna call it a day!")
    elif total_study_time > 2 * 60:
        print("Is that all for today?")
    elif total_study_time < 2 * 60:
        print("You could take a break then come back fresh for the next session!")
    
    # Connect to database
    db = sqlite3.connect(DB_PATH)
    cr = db.cursor()
    # Recording session duration
    cr.execute("UPDATE sessions SET duration = ? where session_id = ?", (total_study_time, session_id))

    # Saving and closing database
    db.commit()
    db.close()


if __name__ == "__main__":
    main()