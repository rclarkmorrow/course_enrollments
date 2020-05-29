""" ---------------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------------"""


# Standard library dependencies
from types import SimpleNamespace

# Local application dependencies
from database.models import Enrollment


""" ---------------------------------------------------------------------------
# TEST DATA CLASS
# --------------------------------------------------------------------------"""


# Class initializes with test data, and methods to populate test database.
# -----------------------------------------------------------------------------
class EnrollmentTest:
    def __init__(self):
        # Seed data for test database
        self.seeds = [
            Enrollment(
                course_uid=1,
                student_uid=1,
            ),
            Enrollment(
                course_uid=2,
                student_uid=2,
            ),
            Enrollment(
                course_uid=3,
                student_uid=3,
            ),
            Enrollment(
                course_uid=4,
                student_uid=4,
            ),
            Enrollment(
                course_uid=5,
                student_uid=5,
            ),
        ]
        # Data for test cases.
        self.data = SimpleNamespace(
            add_enrollment={
                "course_uid": 1,
                "student_uid": 5
            },
            conflict_enrollment={
                "course_uid": 3,
                "student_uid": 1
            },
            duplicate_enrollment={
                "course_uid": 1,
                "student_uid": 1
            },
            bad_id={
                "course_uid": 1,
                "student_uid": "junk"
            },
            bad_course={
                "course_uid": 100000,
                "student_uid": 1
            },
            bad_student={
                "course_uid": 1,
                "student_uid": 100000
            },
            bad_key={
                "course_uid": 1,
                "student_uid": 1,
                "something_bad": "You don't want this in your data."
            },
            missing_key={
                "course_uid": 1

            },
            duplicate={
                "course_uid": 1,
                "student_uid": 1
            },
            conflict={
                "course_uid": 1,
                "student_uid": 1
            }
        )

    # Inserts seed data into database.
    def create_records(self):
        for course in self.seeds:
            course.insert()
