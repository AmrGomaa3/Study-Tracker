# Study Tracker GUI Edition (v2.0)

---
#### Video Demo: https://www.youtube.com/watch?v=Rxmkh5aWxo4
---

## Description

**Study Tracker v1.0** is a command-line based study management application designed to help students and self-learners monitor and analyze their focused study sessions. It provides a secure environment where users can create accounts, start timed study sessions, view personalized statistics, and export their data for review or archiving.

The motivation behind Study Tracker was to address a common problem among learners: staying focused and maintaining healthy study habits. By combining secure user authentication, real-time session tracking, smart break reminders, and analytical feedback, the program offers a full-featured experience that promotes both productivity and well-being. Unlike many basic CLI projects, Study Tracker integrates real-time timekeeping, database persistence, input validation, and testing, all in a single cohesive application.

**Study Tracker v2.0** is a complete graphical redesign of the original command-line version of Study Tracker, a productivity tool designed for students and self-learners to track, manage, and analyze their study habits. This version replaces all text-based interfaces with a full `PyQt5`-based GUI, turning the experience into a visually intuitive and interactive application.

This project was developed after the CLI version was finalized, as a way to extend functionality and explore real-world software development practices including event-driven programming, GUI design, and user-centric layouts. It retains all the backend logic from the original version: secure registration, login, real-time timers, SQLite database storage, and detailed statistics. In addition, layers a complete user interface on top.

The transition from CLI to GUI required rethinking application flow, integrating real-time feedback, managing multiple windows and state transitions, and creating a smooth, user-friendly experience.

---

## Features

### Fully Interactive GUI (PyQt5)

* Multi-window interface using QWidget and QMessageBox.
* Modular navigation: Register, Login, User Menu, Study Timer, Stats.
* Visual layout with labeled buttons, input fields, real-time status updates.
* Provides error dialogs and confirmations.

### Secure User Authentication

* Registration requires username, password, and they cannot be empty or an error message will pop up.
* Password must be re-entered for confirmation.
* Passwords must be at least 6 characters long.
* Passwords are hashed with `bcrypt` before being stored in SQLite.
* Password input fields are masked with echo mode (password dots).
* Login securely checks hashed credentials.

### Real-Time Study Sessions

* Start and track study sessions in real-time with an active timer.
* `QTimer` updates a digital clock every second.
* App warns users after 4 hours to prevent burnout.
* Prompts user to take a break every 50 minutes.
* Automatically tracks break time when user pauses session.
* Users can end sessions manually; duration is saved to local.

### Study Statistics

* Personalized statistics fetched from local database:
  * Total sessions
  * Total and average study time
  * Number of light, normal, and intense sessions
  * Most and least studied subjects
  * Longest session

* Stats are displayed inside a scrollable area.

### CSV Export

* Users can export session history as a `.csv` file using a native file dialog.
* `.csv` file includes session_id, subject, start_time, and duration.

### Testing with Pytest

* Tests include:
  * Password hashing and validation
  * Database creation check

### Account Management

* Users can delete their account permanently.
* Deletion removes both user record and all associated sessions.
* Confirmation prompts to prevent accidental loss.

---

## Libraries used

* `PyQt5` for the GUI.
* `SQLite` for the storage of data in a local database.
* `bcrypt` to hash passwords for a secure data storage.
* `datetime` to handle the timer.
* `os` to define file path.
* `sys` to create the app object required for the GUI.
* `csv` to create csv files.

## File Structure

- project.py          - GUI application using PyQt5
- requirements.txt    - Contains `bcrypt` and `PyQt5`
- test_project.py     - Test suite for critical functions

---

## Design Decisions

### From CLI to GUI

This version is a faithful graphical rewrite of the CLI version. All core logic (registration, login, sessions, stats, export) is preserved but transformed into visual workflows. The choice of `PyQt5` over `TKinter` was made to gain experience with one of the most robust desktop GUI frameworks available for Python.

### Use of databases with `SQLite` over flat files

The use of `SQLite` eased the storage and retrieval of data, as well as the analysis and stats generation.

### User wellness

While studying is important, in the digital world today, for students who are studying online from home, it is so easy to get lost in time and spend hours upon hours studying without noticing. A little interruption with some healthy habits reminder was made to make sure students are able to stay health while still being productive.

### Password hashing

Elected to use `bcrypt` to hash passwords before storing them in the database for a more professional and secure approach.

### Stateless → Stateful

In the CLI version, user interaction was sequential. Here, we track `ID`, `session_id`, break time, and session state across different windows. Navigation required careful management to preserve UX clarity without clutter.

### Feedback and Flow

Pop-ups (QMessageBox) ensure users are notified of errors (e.g., wrong login, incomplete fields) and confirmations (e.g., registration success, export complete). This made GUI feel dynamic and responsive.

### Testing Focus

Testing focused on backend logic — password hashing, database setup. GUI-specific behaviors are harder to test with `pytest`, but effort was made to separate logic and UI to enable future GUI tests.

---

## Future Enhancements

* **User dashboard with calendar view**: Let users browse sessions by date.
* **Charts and graphs**: Add matplotlib integration to visualize study habits.
* **Notifications**: Optional system notifications during breaks or when session ends.
* **Cloud sync**: Let users back up their sessions online.

---

## Windows Executable

A precompiled `.exe` is available on GitHub:

[Download study_tracker.exe](https://github.com/AmrGomaa3/study-tracker/releases/latest)

---

## License

This project is licensed under the [MIT License](LICENSE).  
Feel free to use, modify, and learn from it. Attribution is appreciated.

---

*Thank you for reviewing my project! I hope this graphical version shows not only my technical foundation from CS50P, but also my willingness to push beyond it and explore the world of software design.*
