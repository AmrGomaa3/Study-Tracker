import os
import sqlite3
import csv
from project import hash_password, check_hashed_password, create_database


def test_hash_password():
    pw = "Amr123"
    # Check that the password is hashed
    hashed = hash_password(pw)
    assert hashed != pw
    # Check that hashed password is of type bytes
    assert type(hashed) == bytes


def test_check_hashed_password():
    pw1 = "amr123"
    pw2 = "AMR123"
    hashed_pw_1 = hash_password(pw1)
    # Check that the function correctly compares a password to its hashed version
    assert check_hashed_password(pw1, hashed_pw_1) == True
    assert check_hashed_password(pw2, hashed_pw_1) == False


def test_create_database():
    # Delete any traces of previous database files
    if os.path.exists("study_tracker.db"):
        os.remove("study_tracker.db")

    # Check that database file is created
    create_database()
    assert os.path.exists("study_tracker.db") == True

    # Check that the database contains the correct tables
    db = sqlite3.connect("study_tracker.db")
    cr = db.cursor()
    cr.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cr.fetchall()
    assert ("users",) in tables
    assert ("sessions",) in tables

    # Close the database connection
    db.close()

    # Delete traces of testing
    os.remove("study_tracker.db")