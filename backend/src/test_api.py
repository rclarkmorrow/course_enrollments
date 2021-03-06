""" ---------------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------------"""


# Standard library dependencies
import unittest
import json

# Local application dependencies
from api import create_app
from config.config import db, setup_db, test_database_path
from config.config import STATUS_ERR, SUCCESS, PAGE_LENGTH, TEST_USERS
from helpers.helpers import get_user_token_headers
from database.test_data.courses_data import CourseTest
from database.test_data.students_data import StudentTest
from database.test_data.instructors_data import InstructorTest
from database.test_data.assignments_data import AssignmentTest
from database.test_data.enrollments_data import EnrollmentTest


""" ---------------------------------------------------------------------------
# UNITTEST SETUP
# --------------------------------------------------------------------------"""

# Get token headers for test users.

instructor_token = get_user_token_headers(test_user=TEST_USERS.INSTRUCTOR)
registrar_token = get_user_token_headers(test_user=TEST_USERS.REGISTRAR)
dean_token = get_user_token_headers(test_user=TEST_USERS.DEAN)

# Uncomment to console log tokens.
# print(f'Instructor Token: {instructor_token}')
# print(f'Registrar Token: {registrar_token}')
# print(f'Dean Token: {dean_token}')


# This class represents the course enrollments test case.
class CourseEnrollmentsTestCase(unittest.TestCase):
    # Define test variables and initialize app.
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, test_database_path)
        self.db = db
        # Create app context and database.
        self.app_context = self.app.app_context()
        self.app_context.push()
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
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    """ -----------------------------------------------------------------------
    # STUDENTS ENDPOINT TESTS
    # ----------------------------------------------------------------------"""

    def test_get_students_default_registrar(self):
        """Verifies student records are returned."""
        # Send get request and load results.
        response = self.client().get('/students', headers=registrar_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['students']))
        self.assertTrue(data['students'])

    def test_get_students_default_dean(self):
        """Verifies student records are returned."""
        # Send get request and load results.
        response = self.client().get('/students', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['students']))
        self.assertTrue(data['students'])

    def test_get_students_paginate(self):
        """Verifies student records are returned with pagination."""
        # Send get request and load results.
        response = self.client().get('/students?page=1', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['students']) < PAGE_LENGTH.STUDENTS + 1)
        self.assertTrue(data['total_records'])
        self.assertTrue(data['students'])

    def test_get_students_short(self):
        """Verifies student records returned in short form."""
        # Send get request and load results.
        response = self.client().get(
            '/students?detail=short', headers=dean_token
        )
        data = json.loads(response.data)
        allowed = ['uid', 'name']
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['students']))
        self.assertTrue(data['students'])
        self.assertTrue(self.check_short(data, allowed))

    def test_get_students_full(self):
        """Verifies student records are returned in full form."""
        # Send get request and load results.
        response = self.client().get(
            '/students?detail=full', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['students']))
        self.assertTrue(data['students'])

    def test_401_get_students(self):
        """Verifies 401 error when not authorized."""
        # Send get request and load results.
        response = self.client().get('/students')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_404_students_paginate(self):
        """Verifies 404 error when page is out of range."""
        # Send get request and load results.
        response = self.client().get(
            '/students?page=100000', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORDS)

    def test_405_students_patch_not_allowed(self):
        """Verifies 405 if patch method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().patch(
            '/students', json=self.students.data.edit_student,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_students_put_not_allowed(self):
        """Verifies 405 if put method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().put(
            '/students', json=self.students.data.edit_student,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_students_delete_not_allowed(self):
        """Verifies 405 if delete method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().delete(
            '/students', json=self.students.data.edit_student,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify responsedatetime A combination of a date and a time.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_422_students_invalid_detail(self):
        """Verifies 422 error with invalide detail argument."""
        # Send get request and load results.
        response = self.client().get(
            '/students?detail=junk', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_DETAIL)

    def test_422_students_invalid_page_zero(self):
        """Verifies 422 error when page argument is zero."""
        # Send get request and load results.
        response = self.client().get('/students?page=0', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_PAGE)

    def test_422_students_invalid_page_argument(self):
        """Verifies 422 error when page argument is not integer."""
        # Send get request and load results.
        response = self.client().get('/students?page=junk', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_INT)

    def test_create_student_registrar(self):
        """Verifies creating a new student."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.add_student,
            headers=registrar_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], SUCCESS.STUDENT_CREATED)

    def test_create_student_dean(self):
        """Verifies creating a new student."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.add_student,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], SUCCESS.STUDENT_CREATED)

    def test_401_create_student(self):
        """Verifies 401 error when not authorized."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.add_student)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_422_create_student_missing_key(self):
        """Verifies 422 if student data is missing a key."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.missing_key,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.MISSING_KEY)

    def test_422_create_student_invalid_key(self):
        """Verifies 422 if student data includes invalid key."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.bad_key,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_KEY)

    def test_422_create_student_invalid_phone(self):
        """Verifies 422 if student data includes invalid phone."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.bad_phone,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_PHONE)

    def test_422_create_student_invalid_email(self):
        """Verifies 422 if student data includes invalid email."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.bad_email,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_EMAIL)

    def test_422_create_student_not_unique_email(self):
        """Verifies 422 if student data includes an email
           that is not unique."""
        # Send get request and load results.
        response = self.client().post(
            '/students', json=self.students.data.not_unique_email,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.UNIQUE_EMAIL)

    def test_get_student_registrar(self):
        """Verifies getting a student."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(
            f'/students/{uid}', headers=registrar_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['student'])

    def test_get_student_dean(self):
        """Verifies getting a student."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(f'/students/{uid}', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['student'])

    def test_401_get_student(self):
        """Verifies 401 when not authorized."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(f'/students/{uid}')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_404_get_student(self):
        """Verifies 404 error for non-existent student."""
        # Send get request and load results.
        uid = 100000
        response = self.client().get(f'/students/{uid}', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORD)

    def test_edit_student_registrar(self):
        """Verifies editing a student."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/students/{uid}', json=self.students.data.edit_student,
            headers=registrar_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.STUDENT_EDITED} {uid}')

    def test_edit_student_dean(self):
        """Verifies editing a student."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/students/{uid}', json=self.students.data.edit_student,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.STUDENT_EDITED} {uid}')

    def test_401_edit_student(self):
        """Verifies 401 when not authorized."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/students/{uid}', json=self.students.data.edit_student
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_edit_student_email_self_match(self):
        """Tests editing a student using an email matching current email."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/students/{uid}', json=self.students.data.patch_not_unique_email,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.STUDENT_EDITED} {uid}')

    def test_422_edit_student(self):
        """Verifies 422 editing a student with email that is not unique."""
        # Send get request and load results.
        uid = 2
        response = self.client().patch(
            f'/students/{uid}', json=self.students.data.patch_not_unique_email,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.UNIQUE_EMAIL)

    def test_delete_student_registrar(self):
        """Verifies deleting a student."""
        # Send get request and load results.
        uid = 1
        response = self.client().delete(
            f'/students/{uid}', headers=registrar_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.STUDENT_DELETED} {uid}')

    def test_delete_student_dean(self):
        """Verifies deleting a student."""
        # Send get request and load results.
        uid = 1
        response = self.client().delete(f'/students/{uid}', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.STUDENT_DELETED} {uid}')

    def test_401_delete_student(self):
        """Verifies 401 when not authorized."""
        # Send get request and load results.
        uid = 1
        response = self.client().delete(f'/students/{uid}')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_get_student_with_courses_registrar(self):
        """Verifies getting a student with courses info."""
        # Send get request and load results.
        uid = 2
        response = self.client().get(
            f'/students/{uid}/courses', headers=registrar_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['student'])
        self.assertTrue(data['student']['enrollments'])

    def test_get_student_with_courses_dean(self):
        """Verifies getting a student with courses info."""
        # Send get request and load results.
        uid = 2
        response = self.client().get(
            f'/students/{uid}/courses', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['student'])
        self.assertTrue(data['student']['enrollments'])

    def test_401_get_student_with_courses(self):
        """Verifies 401 when not authorized."""
        # Send get request and load results.
        uid = 2
        response = self.client().get(f'/students/{uid}/courses')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_404_get_student_with_courses(self):
        """Verifies 404 error for non-existent student."""
        # Send get request and load results.
        uid = 100000
        response = self.client().get(
            f'/students/{uid}/courses', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORD)

    def test_405_student_courses_patch_not_allowed(self):
        """Verifies 405 if patch method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().patch(
            '/students/1/courses', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_student_courses_put_not_allowed(self):
        """Verifies 405 if put method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().put('/students/1/courses', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_student_courses_delete_not_allowed(self):
        """Verifies 405 if delete method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().delete(
            '/students/1/courses', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    """ -----------------------------------------------------------------------
    # INSTRUCTORS ENDPOINT TESTS
    # ----------------------------------------------------------------------"""

    def test_get_instructors_default_registrar(self):
        """Verifies instructor records are returned."""
        # Send get request and load results.
        response = self.client().get('/instructors', headers=registrar_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['instructors']))
        self.assertTrue(data['instructors'])

    def test_get_instructors_default_dean(self):
        """Verifies instructor records are returned."""
        # Send get request and load results.
        response = self.client().get('/instructors', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['instructors']))
        self.assertTrue(data['instructors'])

    def test_get_instructors_paginate(self):
        """Verifies instructor records are returned with pagination."""
        # Send get request and load results.
        response = self.client().get('/instructors?page=1', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['instructors']) < PAGE_LENGTH.INSTRUCTORS + 1)
        self.assertTrue(data['total_records'])
        self.assertTrue(data['instructors'])

    def test_get_instructors_short(self):
        """Verifies instructor records returned in short form."""
        # Send get request and load results.
        response = self.client().get(
            '/instructors?detail=short', headers=dean_token
        )
        data = json.loads(response.data)
        allowed = ['uid', 'name', 'bio']
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['instructors']))
        self.assertTrue(data['instructors'])
        self.assertTrue(self.check_short(data, allowed))

    def test_get_instructors_full(self):
        """Verifies instructor records are returned in full form."""
        # Send get request and load results.
        response = self.client().get(
            '/instructors?detail=full', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['instructors']))
        self.assertTrue(data['instructors'])

    def test_401_get_instructors_default(self):
        """Verifies 401 when not authorized."""
        # Send get request and load results.
        response = self.client().get('/instructors')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_404_instructors_paginate(self):
        """Verifies 404 error when page is out of range."""
        # Send get request and load results.
        response = self.client().get(
            '/instructors?page=100000', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORDS)

    def test_405_instructors_patch_not_allowed(self):
        """Verifies 405 if patch method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().patch(
            '/instructors', json=self.instructors.data.edit_instructor,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_instructors_put_not_allowed(self):
        """Verifies 405 if put method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().put(
            '/instructors', json=self.instructors.data.edit_instructor,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_instructors_delete_not_allowed(self):
        """Verifies 405 if delete method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().delete(
            '/instructors', json=self.instructors.data.edit_instructor,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_422_instructors_invalid_detail(self):
        """Verifies 422 error with invalide detail argument."""
        # Send get request and load results.
        response = self.client().get(
            '/instructors?detail=junk', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response,
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_DETAIL)

    def test_422_instructors_invalid_page_zero(self):
        """Verifies 422 error when page argument is zero."""
        # Send get request and load results.
        response = self.client().get('/instructors?page=0', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_PAGE)

    def test_422_instructors_invalid_page_argument(self):
        """Verifies 422 error when page argument is not integer."""
        # Send get request and load results.
        response = self.client().get(
            '/instructors?page=junk', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_INT)

    def test_create_instructor(self):
        """Verifies creating a new instructor."""
        # Send get request and load results.
        response = self.client().post(
            '/instructors', json=self.instructors.data.add_instructor,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], SUCCESS.INSTRUCTOR_CREATED)

    def test_401_create_instructor(self):
        """Verifies 401 when not authorized."""
        # Send get request and load results.
        response = self.client().post(
            '/instructors', json=self.instructors.data.add_instructor
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_422_create_instructor_missing_key(self):
        """Verifies 422 if instructor data is missing a key."""
        # Send get request and load results.
        response = self.client().post(
            '/instructors', json=self.instructors.data.missing_key,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.MISSING_KEY)

    def test_422_create_instructor_invalid_key(self):
        """Verifies 422 if instructor data includes invalid key."""
        # Send get request and load results.
        response = self.client().post(
            '/instructors', json=self.instructors.data.bad_key,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_KEY)

    def test_422_create_instructor_invalid_phone(self):
        """Verifies 422 if instructor data includes invalid phone."""
        # Send get request and load results.
        response = self.client().post(
            '/instructors', json=self.instructors.data.bad_phone,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_PHONE)

    def test_422_create_instructor_invalid_email(self):
        """Verifies 422 if instructor data includes invalid email."""
        # Send get request and load results.
        response = self.client().post(
            '/instructors', json=self.instructors.data.bad_email,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_EMAIL)

    def test_422_create_instructor_not_unique_email(self):
        """Verifies 422 if instructor data includes an email
           that is not unique."""
        # Send get request and load results.
        response = self.client().post(
            '/instructors', json=self.instructors.data.not_unique_email,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.UNIQUE_EMAIL)

    def test_get_instructor_registrar(self):
        """Verifies getting a instructor."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(
            f'/instructors/{uid}', headers=registrar_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['instructor'])

    def test_get_instructor_dean(self):
        """Verifies getting a instructor."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(f'/instructors/{uid}', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['instructor'])

    def test_401_get_instructor(self):
        """Verifies 401 when not authorized."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(f'/instructors/{uid}')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_404_get_instructor(self):
        """Verifies 404 error for non-existent instructor."""
        # Send get request and load results.
        uid = 100000
        response = self.client().get(f'/instructors/{uid}', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORD)

    def test_edit_instructor(self):
        """Verifies editing a instructor."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/instructors/{uid}', json=self.instructors.data.edit_instructor,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.INSTRUCTOR_EDITED} {uid}')

    def test_401_edit_instructor(self):
        """Verifies 401 when not authorized."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/instructors/{uid}', json=self.instructors.data.edit_instructor
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_edit_instructor_email_self_match(self):
        """Verifies 422 editing a instructor with email that is not unique"""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/instructors/{uid}',
            json=self.instructors.data.patch_not_unique_email,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.INSTRUCTOR_EDITED} {uid}')

    def test_422_edit_instructor(self):
        """Verifies 422 editing a instructor with email that is not unique"""
        # Send get request and load results.
        uid = 2
        response = self.client().patch(
            f'/instructors/{uid}',
            json=self.instructors.data.patch_not_unique_email,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.UNIQUE_EMAIL)

    def test_delete_instructor(self):
        """Verifies deleting a instructor."""
        # Send get request and load results.
        uid = 1
        response = self.client().delete(
            f'/instructors/{uid}', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'],
                         f'{SUCCESS.INSTRUCTOR_DELETED} {uid}')

    def test_401_delete_instructor(self):
        """Verifies 401 when not authorized."""
        # Send get request and load results.
        uid = 1
        response = self.client().delete(f'/instructors/{uid}')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_get_instructor_with_courses_registrar(self):
        """Verifies getting an instructor with course info."""
        # Send get request and load results.
        uid = 2
        response = self.client().get(
            f'/instructors/{uid}/courses', headers=registrar_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['instructor'])
        self.assertTrue(data['instructor']['assignments'])

    def test_get_instructor_with_courses_dean(self):
        """Verifies getting an instructor with course info."""
        # Send get request and load results.
        uid = 2
        response = self.client().get(
            f'/instructors/{uid}/courses', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['instructor'])
        self.assertTrue(data['instructor']['assignments'])

    def test_401_get_instructor_with_courses(self):
        """Verifies 401 when not authorized."""
        # Send get request and load results.
        uid = 2
        response = self.client().get(f'/instructors/{uid}/courses')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_404_get_instructor_with_courses(self):
        """Verifies 404 error for non-existent instructor."""
        # Send get request and load results.
        uid = 100000
        response = self.client().get(
            f'/instructors/{uid}/courses', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORD)

    def test_405_instructor_courses_patch_not_allowed(self):
        """Verifies 405 if patch method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().patch(
            '/instructors/1/courses', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_instructor_courses_put_not_allowed(self):
        """Verifies 405 if put method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().put(
            '/instructors/1/courses', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_405_instructor_courses_delete_not_allowed(self):
        """Verifies 405 if delete method attempted on endpoint."""
        # Send get request and load results.
        response = self.client().delete(
            '/instructors/1/courses', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    """ -----------------------------------------------------------------------
    # COURSES ENDPOINT TESTS
    # ----------------------------------------------------------------------"""

    def test_get_courses_default(self):
        """Verifies course records are returned."""
        # Send get request and load results.
        response = self.client().get('/courses')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['courses']))
        self.assertTrue(data['courses'])

    def test_get_courses_paginate(self):
        """Verifies course records are returned with pagination."""
        # Send get request and load results.
        response = self.client().get('/courses?page=1')
        data = json.loads(response.data)
        # Verify response.
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
        # Verify response.
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
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['courses']))
        self.assertTrue(data['courses'])

    def test_404_courses_paginate(self):
        """Verifies 404 error when page is out of range."""
        # Send get request and load results.
        response = self.client().get('/courses?page=100000')
        data = json.loads(response.data)
        # Verify response.
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
        # Verify response.
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
        # Verify response.
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
        # Verify response.
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_405)

    def test_422_courses_invalid_detail(self):
        """Verifies 422 error with invalide detail argument."""
        # Send get request and load results.
        response = self.client().get('/courses?detail=junk')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_DETAIL)

    def test_422_courses_invalid_page_zero(self):
        """Verifies 422 error when page argument is zero."""
        # Send get request and load results.
        response = self.client().get('/courses?page=0')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_PAGE)

    def test_422_courses_invalid_page_argument(self):
        """Verifies 422 error when page argument is not integer."""
        # Send get request and load results.
        response = self.client().get('/courses?page=junk')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_INT)

    def test_create_course_instructor(self):
        """Verifies creating a new course."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.add_course,
            headers=instructor_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], SUCCESS.COURSE_CREATED)

    def test_create_course_dean(self):
        """Verifies creating a new course."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.add_course,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], SUCCESS.COURSE_CREATED)

    def test_401_create_course(self):
        """Verifies 401 when not authorized."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.add_course
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_422_create_course_missing_key(self):
        """Verifies 422 if course data is missing a key."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.missing_key,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.MISSING_KEY)

    def test_422_create_course_invalid_key(self):
        """Verifies 422 if course data includes invalid key."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.bad_key,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_KEY)

    def test_422_create_course_duplicate_day(self):
        """Verifies 422 if course data includes a duplicate day."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.duplicate_day,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.DUP_DAY)

    def test_422_create_course_day_not_list(self):
        """Verifies 422 if course days are not provided as a list."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.day_not_list,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.DAY_LIST)

    def test_422_create_course_invalid_day(self):
        """Verifies 422 if course data includes an invalid day."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.bad_day,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_DAY)

    def test_422_create_course_invalid_start(self):
        """Verifies 422 if course data includes an invalid start time."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.start_early,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.INV_TIME)

    def test_422_create_course_invalid_end(self):
        """Verifies 422 if course data includes an invalid end time."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.start_late,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.INV_TIME)

    def test_422_create_course_start_after_end(self):
        """Verifies 422 if course start time is after end time."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.start_after_end,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.INV_TIME)

    def test_422_create_course_invalid_time(self):
        """Verifies 422 if course data includes an invalid time."""
        # Send get request and load results.
        response = self.client().post(
            '/courses', json=self.courses.data.bad_time,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
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
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['course'])

    def test_404_get_course(self):
        """Verifies 404 error for non-existent course."""
        # Send get request and load results.
        uid = 100000
        response = self.client().get(f'/courses/{uid}')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORD)

    def test_edit_course_instructor(self):
        """Verifies editing a course."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/courses/{uid}', json=self.courses.data.edit_course,
            headers=instructor_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.COURSE_EDITED} {uid}')

    def test_edit_course_dean(self):
        """Verifies editing a course."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/courses/{uid}', json=self.courses.data.edit_course,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.COURSE_EDITED} {uid}')

    def test_edit_course_times(self):
        """Verifies editing a course."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/courses/{uid}', json=self.courses.data.edit_course_time,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.COURSE_EDITED} {uid}')

    def test_401_edit_course(self):
        """Verifies 401 when not authorized"""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/courses/{uid}', json=self.courses.data.edit_course
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_422_edit_course_invalid_start(self):
        """Verifies 422 if course data includes an invalid start time."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/courses/{uid}', json=self.courses.data.start_early,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.INV_TIME)

    def test_422_edit_course_invalid_end(self):
        """Verifies 422 if course data includes an invalid end time."""
        uid = 1
        # Send get request and load results.
        response = self.client().patch(
            f'/courses/{uid}', json=self.courses.data.start_late,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.INV_TIME)

    def test_422_edit_course_start_after_end(self):
        """Verifies 422 if course start time is after end time."""
        uid = 1
        # Send get request and load results.
        response = self.client().patch(
            f'/courses/{uid}', json=self.courses.data.start_after_end,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.INV_TIME)

    def test_422_edit_course_invalid_time(self):
        """Verifies 422 if course data includes an invalid time."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/courses/{uid}', json=self.courses.data.bad_time,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_422)
        self.assertEqual(data['description'], STATUS_ERR.BAD_TIME)

    def test_422_edit_course_conflict(self):
        """Verifies 422 with conflicting assignment."""
        # Send get request and load results.
        uid = 1
        response = self.client().patch(
            f'/courses/{uid}', json=self.courses.data.conflict_time,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_422}')
        self.assertEqual(data['description'], f'{STATUS_ERR.CONFLICT}')

    def test_delete_course(self):
        """Verifies deleting a course."""
        # Send get request and load results.
        uid = 1
        response = self.client().delete(f'/courses/{uid}', headers=dean_token)
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.COURSE_DELETED} {uid}')

    def test_401_delete_course(self):
        """Verifies 401 when not authorized."""
        # Send get request and load results.
        uid = 1
        response = self.client().delete(f'/courses/{uid}')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_get_course_with_students_registrar(self):
        """Verifies getting a course with students info."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(
            f'/courses/{uid}/students', headers=registrar_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['course'])
        self.assertTrue(data['course']['students'])

    def test_get_course_with_students_dean(self):
        """Verifies getting a course with students info."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(
            f'/courses/{uid}/students', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['course'])
        self.assertTrue(data['course']['students'])

    def test_404_get_course_with_students(self):
        """Verifies 404 error for non-existent course."""
        # Send get request and load results.
        uid = 100000
        response = self.client().get(
            f'/courses/{uid}/students', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORD)

    def test_get_course_with_instructors_registrar(self):
        """Verifies getting a course with instructors info."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(
            f'/courses/{uid}/instructors', headers=registrar_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['course'])
        self.assertTrue(data['course']['instructors'])

    def test_get_course_with_instructors_dean(self):
        """Verifies getting a course with instructors info."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(
            f'/courses/{uid}/instructors', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['course'])
        self.assertTrue(data['course']['instructors'])

    def test_401_get_course_with_instructors(self):
        """Verifies 401 not authorized."""
        # Send get request and load results.
        uid = 1
        response = self.client().get(f'/courses/{uid}/instructors')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_404_get_course_with_instructors(self):
        """Verifies 404 error for non-existent course."""
        # Send get request and load results.
        uid = 100000
        response = self.client().get(
            f'/courses/{uid}/instructors', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_404)
        self.assertEqual(data['description'], STATUS_ERR.NO_RECORD)

    """ -----------------------------------------------------------------------
    # ASSIGNMENTS ENDPOINT TESTS
    # ----------------------------------------------------------------------"""

    def test_post_assignment(self):
        """Verifies assignment can be posted."""
        # Send get request and load results.
        response = self.client().post(
            '/assignments', json=self.assignments.data.add_assignment,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.ASSIGNMENT_CREATED}')

    def test_401_post_assignment(self):
        """Verifies 401 not authorized."""
        # Send get request and load results.
        response = self.client().post(
            '/assignments', json=self.assignments.data.add_assignment
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_422_post_assignment_duplicate(self):
        """Verifies 422 with duplicate assignment."""
        # Send get request and load results.
        response = self.client().post(
            '/assignments', json=self.assignments.data.duplicate_assignment,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_422}')
        self.assertEqual(data['description'], f'{STATUS_ERR.DUPLICATE}')

    def test_422_post_assignment_conflict(self):
        """Verifies 422 with conflicting assignment."""
        # Send get request and load results.
        response = self.client().post(
            '/assignments', json=self.assignments.data.conflict_assignment,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_422}')
        self.assertEqual(data['description'], f'{STATUS_ERR.CONFLICT}')

    def test_422_post_assignment_id_str(self):
        """Verifies 422 with bad course ID."""
        # Send get request and load results.
        response = self.client().post(
            '/assignments', json=self.assignments.data.bad_id,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_422}')
        self.assertEqual(data['description'], f'{STATUS_ERR.BAD_INT}')

    def test_422_post_assignment_course(self):
        """Verifies 422 with non-existent ID."""
        # Send get request and load results.
        response = self.client().post(
            '/assignments', json=self.assignments.data.bad_course,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_404}')
        self.assertEqual(data['description'], f'{STATUS_ERR.NO_RECORD}')

    def test_422_post_assignment_instructor(self):
        """Verifies 422 with non-existent instructor ID."""
        # Send get request and load results.
        response = self.client().post(
            '/assignments', json=self.assignments.data.bad_instructor,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_404}')
        self.assertEqual(data['description'], f'{STATUS_ERR.NO_RECORD}')

    def test_delete_assignment(self):
        """Verifies deleting assignment by uid."""
        # Send get request and load results.
        uid = 1
        response = self.client().delete(
            f'/assignments/{uid}', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(
            data['message'], f'{SUCCESS.ASSIGNMENT_DELETED} {uid}'
        )

    def test_401_delete_assignment(self):
        """Verifies 401 not authorized."""
        # Send get request and load results.
        uid = 1
        response = self.client().delete(f'/assignments/{uid}')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_404_delete_assignment(self):
        """Verifies 404 deleting non-existent assignment."""
        # Send get request and load results.
        uid = 100000
        response = self.client().delete(
            f'/assignments/{uid}', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_404}')

    """ -----------------------------------------------------------------------
    # ENROLLMENTS ENDPOINT TESTS
    # ----------------------------------------------------------------------"""

    def test_post_enrollment_registrar(self):
        """Verifies enrollment can be posted."""
        # Send get request and load results.
        response = self.client().post(
            '/enrollments', json=self.enrollments.data.add_enrollment,
            headers=registrar_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.ENROLLMENT_CREATED}')

    def test_post_enrollment_dean(self):
        """Verifies enrollment can be posted."""
        # Send get request and load results.
        response = self.client().post(
            '/enrollments', json=self.enrollments.data.add_enrollment,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'{SUCCESS.ENROLLMENT_CREATED}')

    def test_401_post_enrollment_dean(self):
        """Verifies 401 not authorized."""
        # Send get request and load results.
        response = self.client().post(
            '/enrollments', json=self.enrollments.data.add_enrollment
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_404_post_enrollment_course(self):
        """Verifies 422 with bad course ID"""
        # Send get request and load results.
        response = self.client().post(
            '/enrollments', json=self.enrollments.data.bad_course,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_404}')
        self.assertEqual(data['description'], f'{STATUS_ERR.NO_RECORD}')

    def test_404_post_enrollment_student(self):
        """Verifies 422 with bad student ID."""
        # Send get request and load results.
        response = self.client().post(
            '/enrollments', json=self.enrollments.data.bad_student,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_404}')
        self.assertEqual(data['description'], f'{STATUS_ERR.NO_RECORD}')

    def test_422_post_enrollment_duplicate(self):
        """Verifies 422 with duplicate enrollment."""
        # Send get request and load results.
        response = self.client().post(
            '/enrollments', json=self.enrollments.data.duplicate_enrollment,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_422}')
        self.assertEqual(data['description'], f'{STATUS_ERR.DUPLICATE}')

    def test_422_post_enrollment_conflict(self):
        """Verifies 422 with conflicting enrolllment."""
        # Send get request and load results.
        response = self.client().post(
            '/enrollments', json=self.enrollments.data.conflict_enrollment,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_422}')
        self.assertEqual(data['description'], f'{STATUS_ERR.CONFLICT}')

    def test_422_post_enrollment_id_str(self):
        """Verifies 422 with bad ID"""
        # Send get request and load results.
        response = self.client().post(
            '/enrollments', json=self.enrollments.data.bad_id,
            headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_422}')
        self.assertEqual(data['description'], f'{STATUS_ERR.BAD_INT}')

    def test_delete_enrollment_registrar(self):
        """Verifies delete enrollment record by uid."""
        # Send get request and load results.
        uid = '1'
        response = self.client().delete(
            f'/enrollments/{uid}', headers=registrar_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(
            data['message'], f'{SUCCESS.ENROLLMENT_DELETED} {uid}'
        )

    def test_delete_enrollment_dean(self):
        """Verifies delete enrollment record by uid."""
        # Send get request and load results.
        uid = '1'
        response = self.client().delete(
            f'/enrollments/{uid}', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(
            data['message'], f'{SUCCESS.ENROLLMENT_DELETED} {uid}'
        )

    def test_401_delete_enrollment_dean(self):
        """Verifies delete enrollment record by uid."""
        # Send get request and load results.
        uid = '1'
        response = self.client().delete(f'/enrollments/{uid}')
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], STATUS_ERR.CODE_401)

    def test_404_delete_enrollment(self):
        """Verifies 404 deleting non-existent enrollment."""
        # Send get request and load results.
        uid = 100000
        response = self.client().delete(
            f'/enrollments/{uid}', headers=dean_token
        )
        data = json.loads(response.data)
        # Verify response.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'{STATUS_ERR.CODE_404}')


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
