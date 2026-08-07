# Student Management System

A full-stack mini-project: Python (Flask) + SQLite, with a Bootstrap web UI.
Manages **Students**, **Courses**, and **Enrollments** (many-to-many between
students and courses, with semester + grade).

## Features
- Add / edit / delete students
- Add / delete courses
- Enroll a student in a course (with semester and grade)
- Dashboard with live counts
- Sample data seeded automatically on first run

## Project structure
```
student_management/
├── app.py                 # Flask app & routes
├── database.py             # Schema (students, courses, enrollments) + sample data
├── requirements.txt
├── templates/               # Jinja2 + Bootstrap templates
│   ├── base.html
│   ├── index.html
│   ├── students.html
│   ├── student_form.html
│   ├── courses.html
│   ├── course_form.html
│   ├── enrollments.html
│   └── enrollment_form.html
└── student_management.db   # created automatically on first run
```

## Database schema
```
students(student_id PK, first_name, last_name, email UNIQUE, phone,
         date_of_birth, gender, address, enrollment_date)

courses(course_id PK, course_code UNIQUE, course_name, credits, instructor)

enrollments(enrollment_id PK, student_id FK -> students,
            course_id FK -> courses, semester, grade)
```
`enrollments` is the join table resolving the many-to-many relationship
between students and courses.

## Setup

1. Make sure Python 3.9+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open your browser at **http://127.0.0.1:5000**

The database file (`student_management.db`) is created automatically the
first time you run the app, along with a few sample rows so the UI isn't
empty.

## Resetting the database
Delete `student_management.db` and re-run `python app.py` — it will be
recreated with fresh sample data.

## Extending it
Some natural next steps if you want to expand this for a college project
or portfolio piece:
- Add authentication (admin login) using Flask-Login
- Add search/filter on the students and courses pages
- Export student lists to CSV or PDF
- Add attendance tracking as a new table
- Switch SQLite → MySQL/PostgreSQL for a production deployment
- Add REST API endpoints (return JSON) alongside the HTML views
