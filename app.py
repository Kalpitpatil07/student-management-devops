import os
from flask import Flask, request, redirect, url_for, render_template_string, flash
from student_service import StudentService, CourseService, FacultyService, EnrollmentService, MarksService, init_db

DB_PATH = os.environ.get("DATABASE_PATH", "student_management.db")
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")
init_db(DB_PATH)

def services():
    return (
        StudentService(DB_PATH), CourseService(DB_PATH), FacultyService(DB_PATH),
        EnrollmentService(DB_PATH), MarksService(DB_PATH)
    )

BASE_HTML = """
<!doctype html><html lang="en"><head><meta charset="utf-8">
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Student Management Platform</title>

    <style>
        <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Student Management Platform</title>
    <style>
        body {
            background: #f4f6fb;
            font-family: "Segoe UI", Arial, sans-serif;
        }
    </style>
</head>
    </style>
</head>

@app.route("/")
def index():
    students, courses, faculty, enrollments, marks = services()

    return render_template_string(
        BASE_HTML.replace(
            "{% block body %}{% endblock %}",
            """
            <section>
                <h2>Dashboard</h2>
                <p>Manage student records, courses, faculty,
                course enrollments, marks, and GPA.</p>
                <ul>
                    <li>Students: {{ students }}</li>
                    <li>Courses: {{ courses }}</li>
                    <li>Faculty: {{ faculty }}</li>
                    <li>Enrollments: {{ enrollments }}</li>
                    <li>Marks records: {{ marks }}</li>
                </ul>
                <p>Health endpoint:
                <a href="/health">/health</a></p>
            </section>
            """
        ),
        students=len(students.list()),
        courses=len(courses.list()),
        faculty=len(faculty.list()),
        enrollments=len(enrollments.list()),
        marks=len(marks.list())
    )

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/students", methods=["GET", "POST"])
def students_page():
    students, *_ = services()
    if request.method == "POST":
        try:
            students.create(request.form.get("name", ""), request.form.get("email", ""), request.form.get("prn", ""))
            flash("Student added successfully.")
        except ValueError as e:
            flash(str(e))
        return redirect(url_for("students_page"))
    rows = students.list()
    return render_template_string(BASE_HTML + """
    {% block body %}<section><h2>Add student</h2><form method="post">
    <input name="name" placeholder="Full name" required>
    <input name="email" type="email" placeholder="Email" required>
    <input name="prn" placeholder="PRN / Student ID" required><button>Add student</button></form></section>
    <section><h2>Student records</h2><table><tr><th>ID</th><th>Name</th><th>Email</th><th>PRN</th></tr>
    {% for s in rows %}<tr><td>{{s['id']}}</td><td>{{s['name']}}</td><td>{{s['email']}}</td><td>{{s['prn']}}</td></tr>{% else %}
    <tr><td colspan="4">No students yet.</td></tr>{% endfor %}</table></section>{% endblock %}
    """, rows=rows)

@app.route("/courses", methods=["GET", "POST"])
def courses_page():
    _, courses, *_ = services()
    if request.method == "POST":
        try:
            courses.create(request.form.get("code", ""), request.form.get("title", ""), request.form.get("credits", ""))
            flash("Course added successfully.")
        except ValueError as e:
            flash(str(e))
        return redirect(url_for("courses_page"))
    return render_template_string(BASE_HTML + """
    {% block body %}<section><h2>Add course</h2><form method="post">
    <input name="code" placeholder="Course code" required><input name="title" placeholder="Course title" required>
    <input name="credits" type="number" min="1" max="10" placeholder="Credits" required><button>Add course</button></form></section>
    <section><h2>Courses</h2><table><tr><th>ID</th><th>Code</th><th>Title</th><th>Credits</th></tr>
    {% for c in rows %}<tr><td>{{c['id']}}</td><td>{{c['code']}}</td><td>{{c['title']}}</td><td>{{c['credits']}}</td></tr>
    {% else %}<tr><td colspan="4">No courses yet.</td></tr>{% endfor %}</table></section>{% endblock %}
    """, rows=courses.list())

@app.route("/faculty", methods=["GET", "POST"])
def faculty_page():
    *_, faculty, enrollments, marks = services()
    if request.method == "POST":
        try:
            faculty.create(request.form.get("name", ""), request.form.get("email", ""), request.form.get("department", ""))
            flash("Faculty member added successfully.")
        except ValueError as e:
            flash(str(e))
        return redirect(url_for("faculty_page"))
    return render_template_string(BASE_HTML + """
    {% block body %}<section><h2>Add faculty</h2><form method="post">
    <input name="name" placeholder="Full name" required><input name="email" type="email" placeholder="Email" required>
    <input name="department" placeholder="Department" required><button>Add faculty</button></form></section>
    <section><h2>Faculty</h2><table><tr><th>ID</th><th>Name</th><th>Email</th><th>Department</th></tr>
    {% for f in rows %}<tr><td>{{f['id']}}</td><td>{{f['name']}}</td><td>{{f['email']}}</td><td>{{f['department']}}</td></tr>
    {% else %}<tr><td colspan="4">No faculty yet.</td></tr>{% endfor %}</table></section>{% endblock %}
    """, rows=faculty.list())

@app.route("/enrollments", methods=["GET", "POST"])
def enrollments_page():
    students, courses, faculty, enrollments, marks = services()
    if request.method == "POST":
        try:
            enrollments.create(request.form.get("student_id", ""), request.form.get("course_id", ""))
            flash("Enrollment created.")
        except ValueError as e:
            flash(str(e))
        return redirect(url_for("enrollments_page"))
    return render_template_string(BASE_HTML + """
    {% block body %}<section><h2>Enroll student in course</h2><form method="post">
    <label>Student</label><select name="student_id" required>{% for s in students %}<option value="{{s['id']}}">{{s['prn']}} — {{s['name']}}</option>{% endfor %}</select>
    <label>Course</label><select name="course_id" required>{% for c in courses %}<option value="{{c['id']}}">{{c['code']}} — {{c['title']}}</option>{% endfor %}</select>
    <button>Enroll</button></form><p>Add students and courses before enrolling.</p></section>
    <section><h2>Enrollments</h2><table><tr><th>ID</th><th>Student</th><th>Course</th></tr>
    {% for e in rows %}<tr><td>{{e['id']}}</td><td>{{e['student_name']}} ({{e['prn']}})</td><td>{{e['course_code']}} — {{e['course_title']}}</td></tr>
    {% else %}<tr><td colspan="3">No enrollments yet.</td></tr>{% endfor %}</table></section>{% endblock %}
    """, students=students.list(), courses=courses.list(), rows=enrollments.list())

@app.route("/marks", methods=["GET", "POST"])
def marks_page():
    students, courses, faculty, enrollments, marks = services()
    if request.method == "POST":
        try:
            marks.create(request.form.get("student_id", ""), request.form.get("course_id", ""), request.form.get("score", ""))
            flash("Marks saved.")
        except ValueError as e:
            flash(str(e))
        return redirect(url_for("marks_page"))
    rows = marks.list()
    return render_template_string(BASE_HTML + """
    {% block body %}<section><h2>Record marks</h2><form method="post">
    <label>Student</label><select name="student_id" required>{% for s in students %}<option value="{{s['id']}}">{{s['prn']}} — {{s['name']}}</option>{% endfor %}</select>
    <label>Course</label><select name="course_id" required>{% for c in courses %}<option value="{{c['id']}}">{{c['code']}} — {{c['title']}}</option>{% endfor %}</select>
    <input name="score" type="number" min="0" max="100" step="0.01" placeholder="Score (0-100)" required><button>Save marks</button>
    </form></section><section><h2>Marks and GPA</h2><table><tr><th>Student</th><th>Course</th><th>Score</th><th>Grade points</th></tr>
    {% for m in rows %}<tr><td>{{m['student_name']}}</td><td>{{m['course_code']}}</td><td>{{m['score']}}</td><td>{{m['grade_points']}}</td></tr>
    {% else %}<tr><td colspan="4">No marks yet.</td></tr>{% endfor %}</table>
    <h3>Student GPA</h3>{% for g in gpas %}<p>{{g['name']}} ({{g['prn']}}): {{g['gpa']}}</p>{% else %}<p>GPA appears after marks are recorded.</p>{% endfor %}
    <p><small>Example grading rule: 90+=10, 80–89=9, 70–79=8, 60–69=7, 50–59=6, 40–49=5, below 40=0. Confirm your college's grading scheme before academic use.</small></p>
    </section>{% endblock %}
    """, students=students.list(), courses=courses.list(), rows=rows, gpas=marks.gpas())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
