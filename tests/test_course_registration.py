import pytest
from student_service import StudentService, CourseService, EnrollmentService

def test_student_can_enroll_in_course(tmp_path):
    db = str(tmp_path / "test.db")
    student_id = StudentService(db).create("Asha", "asha@example.com", "PRN001")
    course_id = CourseService(db).create("CS101", "Programming", 4)
    service = EnrollmentService(db)
    service.create(student_id, course_id)
    assert len(service.list()) == 1
    assert service.list()[0]["course_code"] == "CS101"

def test_duplicate_enrollment_is_rejected(tmp_path):
    db = str(tmp_path / "test.db")
    student_id = StudentService(db).create("Asha", "asha@example.com", "PRN001")
    course_id = CourseService(db).create("CS101", "Programming", 4)
    service = EnrollmentService(db)
    service.create(student_id, course_id)
    with pytest.raises(ValueError, match="already enrolled"):
        service.create(student_id, course_id)

def test_enrollment_requires_existing_student_and_course(tmp_path):
    with pytest.raises(ValueError, match="Student does not exist"):
        EnrollmentService(str(tmp_path / "test.db")).create(99, 1)
