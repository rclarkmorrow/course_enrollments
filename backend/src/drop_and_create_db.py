""" ---------------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------------"""


# Standard library dependencies
import unittest
import json

# Local application dependencies
from api import create_app
from config.config import db, setup_db
from database.test_data.courses_data import CourseTest
from database.test_data.students_data import StudentTest
from database.test_data.instructors_data import InstructorTest
from database.test_data.assignments_data import AssignmentTest
from database.test_data.enrollments_data import EnrollmentTest


""" ---------------------------------------------------------------------------
# UNITTEST SETUP
# --------------------------------------------------------------------------"""


# This class represents the course enrollments test case.
class CourseEnrollmentsTestCase(unittest.TestCase):
    # Define test variables and initialize app.
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        self.db = db
        # Create app context and database.
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.drop_all()
        self.db.create_all()
        # Add test course records to test database.
        self.courses = CourseTest()
        self.courses.create_records()
        # Add test student records to test database.
        self.students = StudentTest()
        self.students.create_records()
        # Add test instructor records to test database.
        self.instructors = InstructorTest()
        self.instructors.create_records()
        # Add test assignment records to test database.
        self.assignments = AssignmentTest()
        self.assignments.create_records()
        # Add test enrollments records to test database.
        self.enrollments = EnrollmentTest()
        self.enrollments.create_records()

    # Remove session, drop db tables and tear down app context.
    def tearDown(self):
        self.db.session.remove()
        self.app_context.pop()

    """ -----------------------------------------------------------------------
    # GENERAL TESTS
    # ----------------------------------------------------------------------"""

    def test_general(self):
        """Verifies site is up"""
        # Send get request and load results.
        response = self.client().get('/')
        # Verify response.
        self.assertEqual(response.status_code, 200)


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
