""" ---------------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------------"""


# Standard library dependencies
import unittest
import json
from types import SimpleNamespace  # NOTE: delete if unused.

# Third party dependencies
from flask_sqlalchemy import SQLAlchemy

# Local application dependencies
from api import create_app
from config.config import db, setup_db, create_test_db_path
from config.config import STATUS_ERR, SUCCESS
from database.test_data.courses_data import CourseTest



""" ---------------------------------------------------------------------------
# UNITTEST SETUP
# --------------------------------------------------------------------------"""


# This class represents the course enrollments test case.
class CourseEnrollmentsTestCase(unittest.TestCase):
    # Define test variables and initialize app.
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = create_test_db_path()
        setup_db(self.app, self.database_path)
        self.db = db
        # Create app context.
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.create_all()
        # Add test course records to test database.
        self.courses = CourseTest()
        self.courses.create_records()

    # Remove session, drop db tables and tear down app context.
    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

    # Checks that response doesn't include more keys than allowed
    # when short records are requested.
    def check_short(self, data, allowed):
        check_passed = True
        for key, value in data.items():
            if type(value) is list:
                for item in value:
                    for key, value in item.items():
                        if key not in allowed:
                            check_passed = False
        return check_passed

    """ -----------------------------------------------------------------------
    # GENERAL TESTS
    # ----------------------------------------------------------------------"""

    def test_general_404(self):
        """Verifies 404 response from non-existent endpoint."""
        # Send get request and load results.
        response = self.client().get('/bad_endpoint')
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    """ -----------------------------------------------------------------------
    # COURSES ENDPOINT TESTS
    # ----------------------------------------------------------------------"""

    def test_get_courses_default(self):
        """Verifies course records are returned."""
        # Send get request and load results.
        response = self.client().get('/courses')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['courses']))
        self.assertTrue(data['courses'])

    def test_get_courses_short(self):
        """Verifies course records returned in short form."""
        # Send get request and load results.
        response = self.client().get('/courses?detail=short')
        data = json.loads(response.data)
        allowed = ['uid', 'title']
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['courses']))
        self.assertTrue(data['courses'])
        self.assertTrue(self.check_short(data, allowed))
        # self.assertFalse(data['courses'].get('days'))

    def test_get_courses_full(self):
        """Verifies course records are returned."""
        # Send get request and load results.
        response = self.client().get('/courses?detail=full')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['courses']))
        self.assertTrue(data['courses'])

    def test_create_course(self):
        """Verifies creating a new course."""
        # Send get request and load results.
        response = self.client().post('/courses',
                                      json=self.courses.data.add_course)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], SUCCESS.COURSE_CREATED)

    def test_405_course_patch_not_allowed(self):
        """Verifies 405 if patch method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().patch('/courses',
                                       json=self.courses.data.edit_course)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_course_put_not_allowed(self):
        """Verifies 405 if put method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().put('/courses',
                                     json=self.courses.data.edit_course)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_course_delete_not_allowed(self):
        """Verifies 405 if delete method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().delete('/courses',
                                        json=self.courses.data.edit_course)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_422_create_course_missing_key(self):
        """Verifies 422 if course data is missing a key."""
        # Send get request and load results.
        response = self.client().post('/courses',
                                      json=self.courses.data.missing_key)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.MISSING_KEY)

    def test_422_create_course_invalid_key(self):
        """Verifies 422 if course data includes invalid key."""
        # Send get request and load results.
        response = self.client().post('/courses',
                                      json=self.courses.data.bad_key)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_KEY)

    def test_422_create_course_duplicate_day(self):
        """Verifies 422 if course data includes a duplicate day."""
        # Send get request and load results.
        response = self.client().post('/courses',
                                      json=self.courses.data.duplicate_day)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.DUP_DAY)

    def test_422_create_course_day_not_list(self):
        """Verifies 422 if course days are not provided as a list."""
        # Send get request and load results.
        response = self.client().post('/courses',
                                      json=self.courses.data.day_not_list)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.DAY_LIST)

    def test_422_create_course_invalid_day(self):
        """Verifies 422 if course data includes an invalid day."""
        # Send get request and load results.
        response = self.client().post('/courses',
                                      json=self.courses.data.bad_day)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_DAY)

    def test_422_create_course_invalid_start(self):
        """Verifies 422 if course data includes an invalid start time."""
        # Send get request and load results.
        response = self.client().post('/courses',
                                      json=self.courses.data.start_early)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.INV_TIME)

    def test_422_create_course_invalid_end(self):
        """Verifies 422 if course data includes an invalid end time."""
        # Send get request and load results.
        response = self.client().post('/courses',
                                      json=self.courses.data.start_late)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.INV_TIME)

    def test_422_create_course_start_after_end(self):
        """Verifies 422 if course start time is after end time."""
        # Send get request and load results.
        response = self.client().post('/courses',
                                      json=self.courses.data.start_after_end)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.INV_TIME)

    def test_422_create_course_invalid_time(self):
        """Verifies 422 if course data includes an invalid time."""
        # Send get request and load results.
        response = self.client().post('/courses',
                                      json=self.courses.data.bad_time)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_TIME)

    def test_get_course(self):
        """Verifies editing a course"""
        # Send get request and load results.
        uid = 1
        response = self.client().get(f'/courses/{uid}')
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['course'])

    def test_edit_course(self):
        """Verifies editing a course"""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(f'/courses/{uid}',
                                       json=self.courses.data.edit_course)
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.COURSE_EDITED} {uid}')

    def test_404_get_course(self):
        """Verifies editing a course"""
        # Send get request and load results.
        uid = 100000
        response = self.client().get(f'/courses/{uid}')
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORD)


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
