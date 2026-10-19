import pytest
from student_service import StudentService

def test_create_and_get_student(tmp_path):
    service = StudentService(str(tmp_path / "test.db"))
    student_id = service.create("Asha Patil", "ASHA@example.com", "PRN001")
    student = service.get(student_id)
    assert student["name"] == "Asha Patil"
    assert student["email"] == "asha@example.com"
    assert student["prn"] == "PRN001"

def test_duplicate_email_or_prn_is_rejected(tmp_path):
    service = StudentService(str(tmp_path / "test.db"))
    service.create("Asha", "asha@example.com", "PRN001")
    with pytest.raises(ValueError, match="already exists"):
        service.create("Ravi", "asha@example.com", "PRN002")

def test_required_fields_are_validated(tmp_path):
    service = StudentService(str(tmp_path / "test.db"))
    with pytest.raises(ValueError, match="required"):
        service.create("", "a@example.com", "PRN001")
