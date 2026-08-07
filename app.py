"""
app.py
Flask web application for the Student Management System.
Run with:  python app.py
Then open: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_connection, init_db, seed_sample_data

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

@app.route("/")
def index():
    conn = get_connection()
    student_count = conn.execute("SELECT COUNT(*) c FROM students").fetchone()["c"]
    course_count = conn.execute("SELECT COUNT(*) c FROM courses").fetchone()["c"]
    enrollment_count = conn.execute("SELECT COUNT(*) c FROM enrollments").fetchone()["c"]
    conn.close()
    return render_template(
        "index.html",
        student_count=student_count,
        course_count=course_count,
        enrollment_count=enrollment_count,
    )


@app.route("/students")
def list_students():
    conn = get_connection()
    students = conn.execute("SELECT * FROM students ORDER BY student_id").fetchall()
    conn.close()
    return render_template("students.html", students=students)


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        data = (
            request.form["first_name"],
            request.form["last_name"],
            request.form["email"],
            request.form.get("phone"),
            request.form.get("date_of_birth"),
            request.form.get("gender"),
            request.form.get("address"),
        )
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO students
                   (first_name, last_name, email, phone, date_of_birth, gender, address)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                data,
            )
            conn.commit()
            flash("Student added successfully.", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            conn.close()
        return redirect(url_for("list_students"))
    return render_template("student_form.html", student=None)


@app.route("/students/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    conn = get_connection()
    if request.method == "POST":
        data = (
            request.form["first_name"],
            request.form["last_name"],
            request.form["email"],
            request.form.get("phone"),
            request.form.get("date_of_birth"),
            request.form.get("gender"),
            request.form.get("address"),
            student_id,
        )
        conn.execute(
            """UPDATE students SET first_name=?, last_name=?, email=?, phone=?,
               date_of_birth=?, gender=?, address=? WHERE student_id=?""",
            data,
        )
        conn.commit()
        conn.close()
        flash("Student updated successfully.", "success")
        return redirect(url_for("list_students"))

    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?", (student_id,)
    ).fetchone()
    conn.close()
    return render_template("student_form.html", student=student)


@app.route("/students/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    conn = get_connection()
    conn.execute("DELETE FROM students WHERE student_id=?", (student_id,))
    conn.commit()
    conn.close()
    flash("Student deleted.", "info")
    return redirect(url_for("list_students"))


# ---------- Courses ----------
@app.route("/courses")
def list_courses():
    conn = get_connection()
    courses = conn.execute("SELECT * FROM courses ORDER BY course_id").fetchall()
    conn.close()
    return render_template("courses.html", courses=courses)


@app.route("/courses/add", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        data = (
            request.form["course_code"],
            request.form["course_name"],
            request.form.get("credits", 3),
            request.form.get("instructor"),
        )
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO courses (course_code, course_name, credits, instructor)
                   VALUES (?, ?, ?, ?)""",
                data,
            )
            conn.commit()
            flash("Course added successfully.", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            conn.close()
        return redirect(url_for("list_courses"))
    return render_template("course_form.html", course=None)


@app.route("/courses/delete/<int:course_id>", methods=["POST"])
def delete_course(course_id):
    conn = get_connection()
    conn.execute("DELETE FROM courses WHERE course_id=?", (course_id,))
    conn.commit()
    conn.close()
    flash("Course deleted.", "info")
    return redirect(url_for("list_courses"))


# ---------- Enrollments ----------
@app.route("/enrollments")
def list_enrollments():
    conn = get_connection()
    rows = conn.execute(
        """SELECT e.enrollment_id, s.first_name || ' ' || s.last_name AS student_name,
                  c.course_name, e.semester, e.grade
           FROM enrollments e
           JOIN students s ON s.student_id = e.student_id
           JOIN courses c ON c.course_id = e.course_id
           ORDER BY e.enrollment_id"""
    ).fetchall()
    conn.close()
    return render_template("enrollments.html", enrollments=rows)


@app.route("/enrollments/add", methods=["GET", "POST"])
def add_enrollment():
    conn = get_connection()
    if request.method == "POST":
        data = (
            request.form["student_id"],
            request.form["course_id"],
            request.form.get("semester"),
            request.form.get("grade") or None,
        )
        try:
            conn.execute(
                """INSERT INTO enrollments (student_id, course_id, semester, grade)
                   VALUES (?, ?, ?, ?)""",
                data,
            )
            conn.commit()
            flash("Enrollment added successfully.", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            conn.close()
        return redirect(url_for("list_enrollments"))

    students = conn.execute("SELECT * FROM students ORDER BY first_name").fetchall()
    courses = conn.execute("SELECT * FROM courses ORDER BY course_name").fetchall()
    conn.close()
    return render_template("enrollment_form.html", students=students, courses=courses)


@app.route("/enrollments/delete/<int:enrollment_id>", methods=["POST"])
def delete_enrollment(enrollment_id):
    conn = get_connection()
    conn.execute("DELETE FROM enrollments WHERE enrollment_id=?", (enrollment_id,))
    conn.commit()
    conn.close()
    flash("Enrollment removed.", "info")
    return redirect(url_for("list_enrollments"))


if __name__ == "__main__":
    init_db()
    seed_sample_data()
    app.run(debug=True)
