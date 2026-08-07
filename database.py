"""
database.py
Handles database connection and schema creation for the
Student Management System.
"""

import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "student_management.db")


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they do not already exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS students (
        student_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name      TEXT NOT NULL,
        last_name       TEXT NOT NULL,
        email           TEXT UNIQUE NOT NULL,
        phone           TEXT,
        date_of_birth   TEXT,
        gender          TEXT,
        address         TEXT,
        enrollment_date TEXT DEFAULT (date('now'))
    );

    CREATE TABLE IF NOT EXISTS courses (
        course_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code   TEXT UNIQUE NOT NULL,
        course_name   TEXT NOT NULL,
        credits       INTEGER NOT NULL DEFAULT 3,
        instructor    TEXT
    );

    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id      INTEGER NOT NULL,
        course_id       INTEGER NOT NULL,
        semester        TEXT,
        grade           TEXT,
        FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE,
        FOREIGN KEY (course_id)  REFERENCES courses (course_id) ON DELETE CASCADE,
        UNIQUE (student_id, course_id, semester)
    );
    """)

    conn.commit()
    conn.close()


def seed_sample_data():
    """Insert a few sample rows so the app isn't empty on first run."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS c FROM students")
    if cur.fetchone()["c"] == 0:
        cur.executemany(
            """INSERT INTO students
               (first_name, last_name, email, phone, date_of_birth, gender, address)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                ("Aarav", "Sharma", "aarav.sharma@example.com", "9876543210",
                 "2003-05-14", "Male", "Pune, Maharashtra"),
                ("Isha", "Verma", "isha.verma@example.com", "9876543211",
                 "2002-11-02", "Female", "Mumbai, Maharashtra"),
                ("Rohan", "Patel", "rohan.patel@example.com", "9876543212",
                 "2003-01-22", "Male", "Ahmedabad, Gujarat"),
            ],
        )

        cur.executemany(
            """INSERT INTO courses (course_code, course_name, credits, instructor)
               VALUES (?, ?, ?, ?)""",
            [
                ("CS101", "Introduction to Programming", 4, "Dr. Mehta"),
                ("CS201", "Database Management Systems", 4, "Dr. Rao"),
                ("MA101", "Discrete Mathematics", 3, "Prof. Iyer"),
            ],
        )

        cur.executemany(
            """INSERT INTO enrollments (student_id, course_id, semester, grade)
               VALUES (?, ?, ?, ?)""",
            [
                (1, 1, "Fall 2025", "A"),
                (1, 2, "Fall 2025", "B+"),
                (2, 1, "Fall 2025", "A-"),
                (3, 3, "Fall 2025", None),
            ],
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    seed_sample_data()
    print("Database initialized at:", DB_NAME)
