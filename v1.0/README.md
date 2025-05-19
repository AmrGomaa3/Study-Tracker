# Study Tracker

---
#### Video Demo: https://www.youtube.com/watch?v=Rxmkh5aWxo4
---

## Description

Study Tracker is a command-line based study management application designed to help students and self-learners monitor and analyze their focused study sessions. It provides a secure environment where users can create accounts, start timed study sessions, view personalized statistics, and export their data for review or archiving.

The motivation behind Study Tracker was to address a common problem among learners: staying focused and maintaining healthy study habits. By combining secure user authentication, real-time session tracking, smart break reminders, and analytical feedback, the program offers a full-featured experience that promotes both productivity and well-being. Unlike many basic CLI projects, Study Tracker integrates real-time timekeeping, database persistence, input validation, and testing, all in a single cohesive application.

---

## Features

### Secure User Authentication
- Users register with a unique username and secure password no less than 6 characters.
- Passwords are hashed using the `bcrypt` algorithm, ensuring that stored credentials are not in plaintext.
- Login requires correct username/password validation against the stored hash.

### Real-Time Study Sessions
- Users can start study sessions tracked in real-time using `datetime` and `time`.
- A live timer updates every second on the terminal, with hours, minutes, and seconds.
- Sessions include automatic reminders:
- Every 50 minutes, users are prompted to take a short break.
- After 4 hours of total study time in one session, the app warns about burnout.

### Detailed Statistics and Feedback
After multiple sessions, users can view:
- Total number of sessions
- Total and average duration (in minutes and hours)
- Number of light (< 2 hrs), normal (2–4 hrs), and intense (> 4 hrs) sessions
- Most and least studied subjects with average and total durations
- Longest single session and subject breakdowns

### Data Export to CSV
- Users may export their complete session history to a CSV file.
- The export includes session IDs, subjects, start times, and durations.
- Useful for tracking progress over time or importing into spreadsheets.

### Account Deletion
- Users can permanently delete their account and all session history.
- This is irreversible and ensures data is not retained post-deletion.

### Testing with Pytest
The project includes a test_project.py file that uses pytest to test:
- Password hashing
- Password validation
- Database creation
- CSV export correctness
Tests are self-contained and avoid interfering with live user data.

---

## Project Files

project.py         Main application logic (menus, DB operations, session flow)
test_project.py    Unit tests for core functions using pytest
requirements.txt   External dependencies list (bcrypt)
study_tracker.db   SQLite database file (created at runtime)
data.csv           Generated CSV export file (on demand)

### project.py
This is the heart of the application and includes all major functions:
main() initializes the program and starts the main menu.
main_menu() presents registration/login options.
register_user() handles validation and bcrypt password hashing.
login_user() validates user credentials against hashed passwords.
user_menu() allows the user to start sessions, view stats, export data, or delete their account.
start_session() and ongoing_session() manage real-time tracking with timer updates, break prompts, and burnout checks.
view_stats() aggregates session data and computes insights.
export_to_csv() creates a CSV file with the user’s session data.
delete_account() removes a user and their sessions from the database.
Utility functions: clear_screen(), hash_password(), check_hashed_password()

### test_project.py
Includes the following test functions:
test_hash_password() - ensures output differs from plain password and returns bytes/string.
test_check_hashed_password() - verifies correct and incorrect password matches.
test_create_database() - ensures tables are created in a new database.
test_export_to_csv() - validates that a test user's session data is correctly written to a CSV.
test_clear_screen() - ensures no exception occurs (smoke test).

---

## Design Decisions

- Password hashing: Elected to use `bcrypt` to hash passwords before storing them in the database for a more professional and secure approach.

- CLI over GUI: While a GUI would have looked much prettier, the decision was made to use CLI to focus more on the python logic and not overcomplicate the project. There are still plans for a GUI in future versions, as well as an executable `.exe` file to mimic a real world windows app.

- Database over flat files: The use of `SQLite` eased the storage and retrieval of data, as well as the analysis and stats generation.

- User wellness: While studying is important, in the digital world today, for students who are studying online from home, it is so easy to get lost in time and spend hours upon hours studying without noticing. A little interruption with some healthy habits reminder was made to make sure students are able to stay health while still being productive.

---

## Future Enhancements

- GUI Interface: A user-friendly GUI for broader accessibility.
- Data Visualization: Integrate matplotlib to display graphs (e.g., time studied per subject).
- Study Goals and Reminders: Daily/weekly targets and alert system.
- Session Notes: Allow users to add notes about each session.
- Multi-user leaderboard: Track stats across users (if extended beyond local).

---

## License

This project is licensed under the [MIT License](LICENSE).  
Feel free to use, modify, and learn from it. Attribution is appreciated.

---
