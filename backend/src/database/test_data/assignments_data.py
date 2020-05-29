""" ---------------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------------"""


# Standard library dependencies
from types import SimpleNamespace

# Local application dependencies
from database.models import Assignment


""" ---------------------------------------------------------------------------
# TEST DATA CLASS
# --------------------------------------------------------------------------"""


# Class initializes with test data, and methods to populate test database.
# -----------------------------------------------------------------------------
class AssignmentTest:
    def __init__(self):
        # Seed data for test database
        self.seeds = [
            Assignment(
                course_uid=1,
                instructor_uid=1,
            ),
            Assignment(
                course_uid=2,
                instructor_uid=2,
            ),
            Assignment(
                course_uid=3,
                instructor_uid=3,
            ),
            Assignment(
                course_uid=4,
                instructor_uid=4,
            ),
            Assignment(
                course_uid=5,
                instructor_uid=5,
            ),
        ]
        # Data for test cases.
        self.data = SimpleNamespace(
            add_assignment={
                "course_uid": 1,
                "instructor_uid": 5
            },
            conflict_assignment={
                "course_uid": 3,
                "instructor_uid": 1
            },
            duplicate_assignment={
                "course_uid": 1,
                "instructor_uid": 1
            },
            bad_id={
                "course_uid": 1,
                "instructor_uid": "junk"
            },
            bad_course={
                "course_uid": 100000,
                "instructor_uid": 1
            },
            bad_instructor={
                "course_uid": 1,
                "instructor_uid": 100000
            },
            bad_key={
                "course_uid": 1,
                "instructor_uid": 1,
                "something_bad": "You don't want this in your data."
            },
            missing_key={
                "course_uid": 1

            },
            duplicate={
                "course_uid": 1,
                "instructor_uid": 1
            },
            conflict={
                "course_uid": 1,
                "instructor_uid": 1
            }
        )

    # Inserts seed data into database.
    def create_records(self):
        for course in self.seeds:
            course.insert()
