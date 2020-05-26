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
from config.config import STATUS_ERR, SUCCESS, PAGE_LENGTH
from database.test_data.courses_data import CourseTest
from database.test_data.students_data import StudentTest



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
        # Add test student records to test database.
        self.students = StudentTest()
        self.students.create_records()

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
    # STUDENTS ENDPOINT TESTS
    # ----------------------------------------------------------------------"""

    def test_get_students_default(self):
        """Verifies student records are returned."""
        # Send get request and load results.
        response = self.client().get('/students')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['students']))
        self.assertTrue(data['students'])

    def test_get_students_paginate(self):
        """Verifies student records are returned with pagination."""
        # Send get request and load results.
        response = self.client().get('/students?page=1')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['students']) < PAGE_LENGTH.STUDENTS + 1)
        self.assertTrue(data['total_records'])
        self.assertTrue(data['students'])

    def test_get_students_short(self):
        """Verifies student records returned in short form."""
        # Send get request and load results.
        response = self.client().get('/students?detail=short')
        data = json.loads(response.data)
        allowed = ['uid', 'name']
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['students']))
        self.assertTrue(data['students'])
        self.assertTrue(self.check_short(data, allowed))

    def test_get_students_full(self):
        """Verifies student records are returned."""
        # Send get request and load results.
        response = self.client().get('/students?detail=full')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['students']))
        self.assertTrue(data['students'])

    def test_404_students_paginate(self):
        """Verifies 404 error when page is out of range."""
        # Send get request and load results.
        response = self.client().get('/students?page=100000')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORDS)

    def test_405_student_patch_not_allowed(self):
        """Verifies 405 if patch method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().patch(
            '/students', json=self.students.data.edit_student
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_student_put_not_allowed(self):
        """Verifies 405 if put method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().put(
            '/students', json=self.students.data.edit_student
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_student_delete_not_allowed(self):
        """Verifies 405 if delete method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().delete(
            '/students', json=self.students.data.edit_student
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_422_students_invalid_detail(self):
        """Verifies 422 error with invalide detail argument."""
        # Send get request and load results.
        response = self.client().get('/students?detail=junk')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_DETAIL)

    def test_422_students_invalid_page_zero(self):
        """Verifies 422 error when page argument is zero."""
        # Send get request and load results.
        response = self.client().get('/students?page=0')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_PAGE)

    def test_422_students_invalid_page_argument(self):
        """Verifies 422 error when page argument is not integer."""
        # Send get request and load results.
        response = self.client().get('/students?page=junk')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_INT)

    def test_create_student(self):
        """Verifies creating a new student."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.add_student
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], SUCCESS.STUDENT_CREATED)

    def test_422_create_student_missing_key(self):
        """Verifies 422 if student data is missing a key."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.missing_key
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.MISSING_KEY)

    def test_422_create_student_invalid_key(self):
        """Verifies 422 if student data includes invalid key."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.bad_key
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_KEY)

    def test_422_create_student_invalid_phone(self):
        """Verifies 422 if student data includes invalid phone."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.bad_phone
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_PHONE)

    def test_422_create_student_invalid_email(self):
        """Verifies 422 if student data includes invalid email."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.bad_email
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_EMAIL)

    def test_422_create_student_not_unique_email(self):
        """Verifies 422 if student data includes an email
           that is not unique."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.not_unique_email
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.UNIQUE_EMAIL)

    def test_get_student(self):
        """Verifies getting a student."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(f'/students/{uid}')
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['student'])

    def test_edit_student(self):
        """Verifies editing a student."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/students/{uid}', json=self.students.data.edit_student
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.STUDENT_EDITED} {uid}')

    def test_edit_student_email_self_match(self):
        """Verifies 422 editing a student with email that is not unique"""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/students/{uid}', json=self.students.data.patch_not_unique_email
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.STUDENT_EDITED} {uid}')

    def test_404_get_student(self):
        """Verifies 404 error for non-existent student."""
        # Send get request and load results.
        uid = 100000
        response = self.client().get(f'/students/{uid}')
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORD)

    def test_422_edit_student(self):
        """Verifies 422 editing a student with email that is not unique"""
        # Send get request and load results.
        uid = 2
        response = self.client().patch(
            f'/students/{uid}', json=self.students.data.patch_not_unique_email
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.UNIQUE_EMAIL)

    def test_delete_student(self):
        """Verifies deleting a student."""
        # Send get request and load results.
        uid = 1
        response = self.client().delete(f'/students/{uid}')
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.STUDENT_DELETED} {uid}')

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

    def test_get_courses_paginate(self):
        """Verifies course records are returned with pagination."""
        # Send get request and load results.
        response = self.client().get('/courses?page=1')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['courses']) < PAGE_LENGTH.COURSES + 1)
        self.assertTrue(data['total_records'])
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

    def test_404_courses_paginate(self):
        """Verifies 404 error when page is out of range."""
        # Send get request and load results.
        response = self.client().get('/courses?page=100000')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORDS)

    def test_405_course_patch_not_allowed(self):
        """Verifies 405 if patch method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().patch(
            '/courses', json=self.courses.data.edit_course
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_course_put_not_allowed(self):
        """Verifies 405 if put method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().put(
            '/courses', json=self.courses.data.edit_course
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_course_delete_not_allowed(self):
        """Verifies 405 if delete method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().delete(
            '/courses', json=self.courses.data.edit_course
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_422_courses_invalid_detail(self):
        """Verifies 422 error with invalide detail argument."""
        # Send get request and load results.
        response = self.client().get('/courses?detail=junk')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_DETAIL)

    def test_422_courses_invalid_page_zero(self):
        """Verifies 422 error when page argument is zero."""
        # Send get request and load results.
        response = self.client().get('/courses?page=0')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_PAGE)

    def test_422_courses_invalid_page_argument(self):
        """Verifies 422 error when page argument is not integer."""
        # Send get request and load results.
        response = self.client().get('/courses?page=junk')
        data = json.loads(response.data)
        # Verify responses
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_INT)

    def test_create_course(self):
        """Verifies creating a new course."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.add_course
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], SUCCESS.COURSE_CREATED)

    def test_422_create_course_missing_key(self):
        """Verifies 422 if course data is missing a key."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.missing_key
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.MISSING_KEY)

    def test_422_create_course_invalid_key(self):
        """Verifies 422 if course data includes invalid key."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.bad_key
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_KEY)

    def test_422_create_course_duplicate_day(self):
        """Verifies 422 if course data includes a duplicate day."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.duplicate_day
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.DUP_DAY)

    def test_422_create_course_day_not_list(self):
        """Verifies 422 if course days are not provided as a list."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.day_not_list
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.DAY_LIST)

    def test_422_create_course_invalid_day(self):
        """Verifies 422 if course data includes an invalid day."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.bad_day
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_DAY)

    def test_422_create_course_invalid_start(self):
        """Verifies 422 if course data includes an invalid start time."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.start_early
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.INV_TIME)

    def test_422_create_course_invalid_end(self):
        """Verifies 422 if course data includes an invalid end time."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.start_late
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.INV_TIME)

    def test_422_create_course_start_after_end(self):
        """Verifies 422 if course start time is after end time."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.start_after_end
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.INV_TIME)

    def test_422_create_course_invalid_time(self):
        """Verifies 422 if course data includes an invalid time."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.bad_time
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_TIME)

    def test_get_course(self):
        """Verifies getting a course."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(f'/courses/{uid}')
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['course'])

    def test_edit_course(self):
        """Verifies editing a course."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/courses/{uid}', json=self.courses.data.edit_course
        )
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.COURSE_EDITED} {uid}')

    def test_404_get_course(self):
        """Verifies 404 error for non-existent course."""
        # Send get request and load results.
        uid = 100000
        response = self.client().get(f'/courses/{uid}')
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORD)

    def test_delete_course(self):
        """Verifies deleting a course."""
        # Send get request and load results.
        uid = 1
        response = self.client().delete(f'/courses/{uid}')
        data = json.loads(response.data)
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.COURSE_DELETED} {uid}')


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
