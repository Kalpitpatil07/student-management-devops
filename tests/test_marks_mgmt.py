import pytest
from student_service import StudentService, CourseService, EnrollmentService, MarksService

def setup_enrolled_student(db):
    student_id = StudentService(db).create("Asha", "asha@example.com", "PRN001")
    course_id = CourseService(db).create("CS101", "Programming", 4)
    EnrollmentService(db).create(student_id, course_id)
    return student_id, course_id

def test_marks_and_gpa(tmp_path):
    db = str(tmp_path / "test.db")
    student_id, course_id = setup_enrolled_student(db)
    service = MarksService(db)
    service.create(student_id, course_id, 85)
    assert service.list()[0]["grade_points"] == 9
    assert service.gpas()[0]["gpa"] == 9.0

def test_marks_range_is_validated(tmp_path):
    db = str(tmp_path / "test.db")
    student_id, course_id = setup_enrolled_student(db)
    with pytest.raises(ValueError, match="between 0 and 100"):
        MarksService(db).create(student_id, course_id, 105)

def test_marks_require_enrollment(tmp_path):
    db = str(tmp_path / "test.db")
    student_id = StudentService(db).create("Asha", "asha@example.com", "PRN001")
    course_id = CourseService(db).create("CS101", "Programming", 4)
    with pytest.raises(ValueError, match="Enroll the student"):
        MarksService(db).create(student_id, course_id, 75)
