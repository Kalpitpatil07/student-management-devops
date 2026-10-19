import sqlite3
from contextlib import contextmanager

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
 id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, prn TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS courses (
 id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT NOT NULL UNIQUE, title TEXT NOT NULL, credits INTEGER NOT NULL CHECK(credits > 0)
);
CREATE TABLE IF NOT EXISTS faculty (
 id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, department TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS enrollments (
 id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL REFERENCES students(id),
 course_id INTEGER NOT NULL REFERENCES courses(id), UNIQUE(student_id, course_id)
);
CREATE TABLE IF NOT EXISTS marks (
 id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL REFERENCES students(id),
 course_id INTEGER NOT NULL REFERENCES courses(id), score REAL NOT NULL CHECK(score >= 0 AND score <= 100),
 UNIQUE(student_id, course_id)
);
"""

def init_db(path="student_management.db"):
    with sqlite3.connect(path) as con:
        con.executescript("PRAGMA foreign_keys = ON;" + SCHEMA)

@contextmanager
def connection(path):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

class StudentService:
    def __init__(self, db_path="student_management.db"):
        self.db_path = db_path
        init_db(db_path)

    def create(self, name, email, prn):
        name, email, prn = name.strip(), email.strip().lower(), prn.strip()
        if not name or not email or not prn:
            raise ValueError("Name, email, and PRN are required.")
        try:
            with connection(self.db_path) as con:
                cur = con.execute("INSERT INTO students(name,email,prn) VALUES(?,?,?)", (name,email,prn))
                return cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Email or PRN already exists.") from None

    def list(self):
        with connection(self.db_path) as con:
            return [dict(r) for r in con.execute("SELECT * FROM students ORDER BY id").fetchall()]

    def get(self, student_id):
        with connection(self.db_path) as con:
            row = con.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
            return dict(row) if row else None

class CourseService:
    def __init__(self, db_path="student_management.db"):
        self.db_path = db_path
        init_db(db_path)

    def create(self, code, title, credits):
        code, title = code.strip().upper(), title.strip()
        if not code or not title:
            raise ValueError("Course code and title are required.")
        try:
            credits = int(credits)
            if not 1 <= credits <= 10:
                raise ValueError("Credits must be between 1 and 10.")
        except (TypeError, ValueError) as exc:
            if isinstance(exc, ValueError) and str(exc) == "Credits must be between 1 and 10.":
                raise
            raise ValueError("Credits must be a whole number between 1 and 10.") from None
        try:
            with connection(self.db_path) as con:
                cur = con.execute("INSERT INTO courses(code,title,credits) VALUES(?,?,?)", (code,title,credits))
                return cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Course code already exists.") from None

    def list(self):
        with connection(self.db_path) as con:
            return [dict(r) for r in con.execute("SELECT * FROM courses ORDER BY id").fetchall()]

class FacultyService:
    def __init__(self, db_path="student_management.db"):
        self.db_path = db_path
        init_db(db_path)

    def create(self, name, email, department):
        name, email, department = name.strip(), email.strip().lower(), department.strip()
        if not name or not email or not department:
            raise ValueError("Name, email, and department are required.")
        try:
            with connection(self.db_path) as con:
                cur = con.execute("INSERT INTO faculty(name,email,department) VALUES(?,?,?)", (name,email,department))
                return cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Faculty email already exists.") from None

    def list(self):
        with connection(self.db_path) as con:
            return [dict(r) for r in con.execute("SELECT * FROM faculty ORDER BY id").fetchall()]

class EnrollmentService:
    def __init__(self, db_path="student_management.db"):
        self.db_path = db_path
        init_db(db_path)

    def create(self, student_id, course_id):
        try:
            student_id, course_id = int(student_id), int(course_id)
        except (TypeError, ValueError):
            raise ValueError("Select a valid student and course.") from None
        try:
            with connection(self.db_path) as con:
                if not con.execute("SELECT 1 FROM students WHERE id=?", (student_id,)).fetchone():
                    raise ValueError("Student does not exist.")
                if not con.execute("SELECT 1 FROM courses WHERE id=?", (course_id,)).fetchone():
                    raise ValueError("Course does not exist.")
                cur = con.execute("INSERT INTO enrollments(student_id,course_id) VALUES(?,?)", (student_id,course_id))
                return cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Student is already enrolled in this course.") from None

    def list(self):
        with connection(self.db_path) as con:
            query = """SELECT e.id, s.name AS student_name, s.prn, c.code AS course_code, c.title AS course_title
                       FROM enrollments e JOIN students s ON s.id=e.student_id JOIN courses c ON c.id=e.course_id
                       ORDER BY e.id"""
            return [dict(r) for r in con.execute(query).fetchall()]

class MarksService:
    def __init__(self, db_path="student_management.db"):
        self.db_path = db_path
        init_db(db_path)

    @staticmethod
    def grade_points(score):
        score = float(score)
        if score >= 90: return 10
        if score >= 80: return 9
        if score >= 70: return 8
        if score >= 60: return 7
        if score >= 50: return 6
        if score >= 40: return 5
        return 0

    def create(self, student_id, course_id, score):
        try:
            student_id, course_id, score = int(student_id), int(course_id), float(score)
        except (TypeError, ValueError):
            raise ValueError("Select a student/course and enter a valid score.") from None
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100.")
        try:
            with connection(self.db_path) as con:
                enrolled = con.execute("SELECT 1 FROM enrollments WHERE student_id=? AND course_id=?", (student_id,course_id)).fetchone()
                if not enrolled:
                    raise ValueError("Enroll the student in the course before entering marks.")
                cur = con.execute("INSERT INTO marks(student_id,course_id,score) VALUES(?,?,?)", (student_id,course_id,score))
                return cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Marks already exist for this student and course.") from None

    def list(self):
        with connection(self.db_path) as con:
            query = """SELECT m.id, s.name AS student_name, s.prn, c.code AS course_code, m.score
                       FROM marks m JOIN students s ON s.id=m.student_id JOIN courses c ON c.id=m.course_id ORDER BY m.id"""
            rows = [dict(r) for r in con.execute(query).fetchall()]
            for row in rows:
                row["grade_points"] = self.grade_points(row["score"])
            return rows

    def gpas(self):
        with connection(self.db_path) as con:
            students = con.execute("SELECT id,name,prn FROM students ORDER BY id").fetchall()
            output = []
            for s in students:
                scores = con.execute("SELECT score FROM marks WHERE student_id=?", (s["id"],)).fetchall()
                if scores:
                    points = [self.grade_points(r["score"]) for r in scores]
                    gpa = round(sum(points) / len(points), 2)
                    output.append({"name": s["name"], "prn": s["prn"], "gpa": gpa})
            return output
