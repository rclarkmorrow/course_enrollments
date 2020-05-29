""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""

# Standard library dependencies
import re
import json  # NOTE: Delete if unused.
from types import SimpleNamespace

# Third party Dependencies
from flask import jsonify

# Local application dependencies
from database.models import (Student, Instructor, Course, Assignment,
                             Enrollment)
from config.config import REGEX, PAGE_LENGTH, SCHEDULE, STATUS_ERR, SUCCESS
from helpers.helpers import StatusError


""" --------------------------------------------------------------------------#
# CONTROLLER CLASSES
# --------------------------------------------------------------------------"""


# A super class that initialises data commonly used by the different
# controller classes and contains commonly used methods.
# -----------------------------------------------------------------------------
class Controller:
    # Init self with data
    def __init__(self, table=None, request_data=None, uid=None):
        self.request_data = request_data
        # print(request_data)
        self.table = table
        self.uid = uid
        if uid:   # When uid is not one, convert to integer.
            self.uid = self.string_to_int(uid)
        self.response_data = SimpleNamespace(success=True)
        self.status = SimpleNamespace(error=False)

    """ BUILDERS
    # ----------------------------------------------------------------------"""
    # Generates JSON response.
    def generate_response(self):
        self.response = jsonify(self.response_data.__dict__), 200

    # Adds records to class object with argument that determines
    # whether the records have full details or truncated details
    # and arguments that determine paginated response.
    def append_records_list(self, table=None, detail='full',
                            page_length=10, page=None):
        # Get all records as a query object.
        query = self.get_all_records()
        self.response_data.total_records = len(query)
        # If page is none, returns all records.
        if page is None:
            start = 0
            stop = None
        # Checks if page can be converted to a positive integer, and
        # paginates response. Otherwise, returns a 422 error.
        else:
            page = self.string_to_int(page)
            if page < 1:
                raise StatusError(
                    STATUS_ERR.CODE_422,
                    STATUS_ERR.BAD_PAGE,
                    422
                )
            start = (page - 1) * page_length
            stop = start + page_length
        # Structure details
        if detail == 'full':
            self.records = (([record.full() for record in query])[start:stop])
        elif detail == 'short':
            self.records = (([record.short() for record in query])[start:stop])
        # Check length of records, error if there are none.
        if len(self.records) < 1:
            raise StatusError(STATUS_ERR.CODE_404, STATUS_ERR.NO_RECORDS, 404)

    """ UTILITY HELPERS
    # ----------------------------------------------------------------------"""
    # Converts a uid passed as a string to an integer value, returns
    # an HTTP error if it is not possible.
    def string_to_int(self, int_string):
        if (type(int_string)) != int:
            try:
                int_string = int(int_string)
                return int_string
            except ValueError:
                raise StatusError(STATUS_ERR.CODE_422, STATUS_ERR.BAD_INT, 422)

    # Converts a time string to an integer value expressed as minutes.
    def time_to_int(self, time_string):
        try:
            time_int = (int(time_string[:2]) * 60) + int(time_string[3:])
        except ValueError:
            raise StatusError(STATUS_ERR.CODE_422, STATUS_ERR.BAD_TIME, 422)
        return time_int

    """ VALIDATION HELPERS
    # ----------------------------------------------------------------------"""
    # Verify that a string representing a time is valid 24-hour time
    # and raise an HTTP error if not.
    def verify_time(self, time_list):
        # If single value passed, convert to list containing single
        # item.
        if type(time_list) != list:
            time_list = [time_list]
        # Loop list to verify time(s).
        for time in time_list:
            if not re.search(
                    r'^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$', time):
                raise StatusError(
                    STATUS_ERR.CODE_422,
                    STATUS_ERR.BAD_TIME,
                    422)

    # Verify that a string represents a valid US phone number.
    def verify_phone(self, phone):
        # Regex validates phone format.
        if (not re.match(REGEX.PHONE_ONE, phone)
                and not re.match(REGEX.PHONE_TWO, phone)):
            raise StatusError(STATUS_ERR.CODE_422, STATUS_ERR.BAD_PHONE, 422)
        # If phone in 123-456-7890 format, take out dashes.
        if len(phone) > 10:
            phone = (phone[:3] + phone[4:7] + phone[8:])
        return phone

    # Verify that a string represents a valid email address.
    def verify_email(self, email):
        # Regex validates email format.
        if not re.search(REGEX.EMAIL, email):
            raise StatusError(STATUS_ERR.CODE_422, STATUS_ERR.BAD_EMAIL, 422)
        # Return email address in lower case.
        return email.lower()

    # Verify request data is valid.
    def verify_request_data(self, valid_keys, strict=False):
        # Verifies that all valid keys are present in the
        # request body.
        if strict is True:
            for data in valid_keys:
                if data not in self.request_data.keys():
                    raise StatusError(
                        STATUS_ERR.CODE_422,
                        STATUS_ERR.MISSING_KEY,
                        422
                    )
        # Verifies that there are no invalid keys present
        # in the request body.
        for key in self.request_data.keys():
            if key not in valid_keys:
                raise StatusError(
                    STATUS_ERR.CODE_422,
                    STATUS_ERR.BAD_KEY,
                    422)

    # Verifies that a value is unique.
    def check_unique(self, key, value, uid=None,
                     message=STATUS_ERR.UNIQUE_GENERIC):
        query = (
            self.table.query
            .filter(getattr(self.table, key)
                    == value).first()
        )
        # If a record is returned and uid doesn't match
        # the uid of the record, raise an error.
        if query is not None and query.uid != uid:
            raise StatusError(STATUS_ERR.CODE_422, message, 422)
    # Verifies that an assignment or enrollment isn't a duplicate and that
    # it doesn't conflict with another assignment or enrollment.
    def verify_schedule(self, course, person):
        for record in person:
            start = record.course.start_time
            end = record.course.end_time
            # Verify unique assignment or enrollment.
            if record.course_uid == self.request_data['course_uid']:
                raise StatusError(STATUS_ERR.CODE_422, STATUS_ERR.DUPLICATE, 422)
            # Verify that there are no scheduling conflicts.
            if ((course.start_time > start
                    and course.start_time < end) or
                    (course.end_time > start and
                        course.end_time < end)):
                raise StatusError(STATUS_ERR.CODE_422, STATUS_ERR.CONFLICT, 422)

    """ DATABASE HELPERS
    # ----------------------------------------------------------------------"""
    # Builds a new record and inserts in the database.
    def create_record(self):
        self.record = self.table()
        for key, value in self.request_data.items():
            if type(value) is str:
                value = value.strip()
            setattr(self.record, key, value)
        self.record.insert()

    def edit_record(self):
        for key, value in self.request_data.items():
            setattr(self.record, key, value)
        self.record.update()

    # Gets record by ID and deletes it.
    def delete_record(self):
        self.get_record_by_id()
        self.record.delete()

    # Get all records from provided table.
    def get_all_records(self):
        if self.table:
            return self.table.query.order_by(self.table.uid).all()
        else:
            raise StatusError(STATUS_ERR.CODE_500, STATUS_ERR.GENERIC, 500)

    # Get a single record by provided table.
    def get_record_by_id(self, table=None, uid=None):
        if not table:
            table = self.table
            uid = self.uid
        self.record = (table.query.filter(table.uid == uid).one_or_none())
        if not self.record:
            raise StatusError(
                STATUS_ERR.CODE_404,
                STATUS_ERR.NO_RECORD,
                404
            )
        return(self.record)

    # Get a course record and a person (Student or Instructor) record from
    # the databalse with provided details.
    def get_course_and_person(self, table, person_uid):
        course = self.get_record_by_id(
                table=Course,
                uid=self.request_data['course_uid']
            )
        person = self.get_record_by_id(
                table=table,
                uid=self.request_data[person_uid]
            )
        if not course or not person:
            raise StatusError(STATUS_ERR.CODE_422, STATUS_ERR.INV_ID, 422)
        return course, person


# Controller class for the Student databale model.
# -----------------------------------------------------------------------------
class Students(Controller):
    # Init self with super.
    def __init__(self, **kwargs):
        super().__init__(table=Student, **kwargs)
        # Set valid keys for student record.
        self.valid_keys = ['name', 'email', 'phone']

    """ ROUTE HANDLERS
    # ----------------------------------------------------------------------"""
    # Returns a list of students. Page length can be configured in config.py
    def list_students(self, detail='full', page_length=PAGE_LENGTH.STUDENTS,
                      page=None):
        self.append_records_list(detail=detail, page_length=page_length,
                                 page=page)
        self.response_data.students = self.records
        self.generate_response()

    # Gets a single student record
    def get_student(self):
        self.get_record_by_id()
        self.response_data.student = self.record.full()
        self.generate_response()

    # Creates a new student record.
    def create_student(self):
        # Verify required keys exist in body of JSON request.
        self.verify_request_data(self.valid_keys, strict=True)
        # Verify phone number and retreieve format for dababase.
        self.request_data['phone'] = self.verify_phone(
            self.request_data['phone']
        )
        # Verify email address and retrieve format for database.
        self.request_data['email'] = self.verify_email(
            self.request_data['email']
        )
        # Verify that email address is unique.
        self.check_unique(key='email', value=self.request_data['email'],
                          message=STATUS_ERR.UNIQUE_EMAIL)
        # Create the student record and insert it.
        self.create_record()
        # Generate response.
        self.response_data.message = SUCCESS.STUDENT_CREATED
        self.generate_response()

    # Updates a student record.
    def edit_student(self):
        # Get the record to edit.
        self.get_record_by_id()
        # Verify valid keys exists in body of JSON request.
        self.verify_request_data(self.valid_keys)
        # If phone in request, verify it and return format for database.
        if 'phone' in self.request_data.keys():
            self.request_data['phone'] = self.verify_phone(
                self.request_data['phone']
            )
        # If email in request, verify it and check that it is unique.
        if 'email' in self.request_data.keys():
            self.request_data['email'] = self.verify_email(
                self.request_data['email']
            )
            self.check_unique(
                key='email',
                value=self.request_data['email'],
                message=STATUS_ERR.UNIQUE_EMAIL,
                uid=self.record.uid
            )
        # Build edits to student record and update it.
        self.edit_record()
        # Generate response.
        self.response_data.message = f'{SUCCESS.STUDENT_EDITED} {self.uid}'
        self.generate_response()

    # Deletes a student record.
    def delete_student(self):
        self.delete_record()
        self.response_data.message = f'{SUCCESS.STUDENT_DELETED} {self.uid}'
        self.generate_response()


# Controller class for the Instructor databale model.
# -----------------------------------------------------------------------------
class Instructors(Controller):
    # Init self with super.
    def __init__(self, **kwargs):
        super().__init__(table=Instructor, **kwargs)
        # Set valid keys for student record.
        self.valid_keys = ['name', 'email', 'phone', 'bio']

    """ ROUTE HANDLERS
    # ----------------------------------------------------------------------"""
    # Returns a list of students. Page length can be configured in config.py
    def list_instructors(self, detail='full',
                         page_length=PAGE_LENGTH.INSTRUCTORS, page=None):
        self.append_records_list(detail=detail, page_length=page_length,
                                 page=page)
        self.response_data.instructors = self.records
        self.generate_response()

    # Gets a single student record
    def get_instructor(self):
        self.get_record_by_id()
        self.response_data.instructor = self.record.full()
        self.generate_response()

    # Creates a new student record.
    def create_instructor(self):
        # Verify required keys exist in body of JSON request.
        self.verify_request_data(self.valid_keys, strict=True)
        # Verify phone number and retreieve format for dababase.
        self.request_data['phone'] = self.verify_phone(
            self.request_data['phone']
        )
        # Verify email address and retrieve format for database.
        self.request_data['email'] = self.verify_email(
            self.request_data['email']
        )
        # Verify that email address is unique.
        self.check_unique(key='email', value=self.request_data['email'],
                          message=STATUS_ERR.UNIQUE_EMAIL)
        # Create the student record and insert it.
        self.create_record()
        # Generate response.
        self.response_data.message = SUCCESS.INSTRUCTOR_CREATED
        self.generate_response()

    # Updates a student record.
    def edit_instructor(self):
        # Get the record to edit.
        self.get_record_by_id()
        # Verify valid keys exists in body of JSON request.
        self.verify_request_data(self.valid_keys)
        # If phone in request, verify it and return format for database.
        if 'phone' in self.request_data.keys():
            self.request_data['phone'] = self.verify_phone(
                self.request_data['phone']
            )
        # If email in request, verify it and check that it is unique.
        if 'email' in self.request_data.keys():
            self.request_data['email'] = self.verify_email(
                self.request_data['email']
            )
            self.check_unique(
                key='email',
                value=self.request_data['email'],
                message=STATUS_ERR.UNIQUE_EMAIL,
                uid=self.record.uid
            )
        # Build edits to student record and update it.
        self.edit_record()
        # Generate response.
        self.response_data.message = f'{SUCCESS.INSTRUCTOR_EDITED} {self.uid}'
        self.generate_response()

    # Deletes a student record.
    def delete_instructor(self):
        self.delete_record()
        self.response_data.message = f'{SUCCESS.INSTRUCTOR_DELETED} {self.uid}'
        self.generate_response()


# Controller class for the Course databale model.
# -----------------------------------------------------------------------------
class Courses(Controller):
    # Init self with super.
    def __init__(self, **kwargs):
        super().__init__(table=Course, **kwargs)
        # Set valid keys for course record.
        self.valid_keys = ['title', 'days', 'description',
                           'start_time', 'end_time']

    """ ROUTE HANDLERS
    # ----------------------------------------------------------------------"""
    # Returns a list of courses. Page length can be configured in config.py.
    def list_courses(self, detail='full', page_length=PAGE_LENGTH.COURSES,
                     page=None):
        self.append_records_list(detail=detail, page_length=page_length,
                                 page=page)
        self.response_data.courses = self.records
        self.generate_response()

    # Gets a single course record
    def get_course(self):
        self.get_record_by_id()
        self.response_data.course = self.record.full()
        self.generate_response()

    # Creates a new course record.
    def create_course(self):
        # Verify required keys exist in body of JSON request.
        self.verify_request_data(self.valid_keys, strict=True)
        # Verify valid days.
        self.verify_days()
        # Verify valid times.
        self.verify_time([self.request_data['start_time'],
                          self.request_data['end_time']])
        # Verify times are valid for scheduling
        self.verify_course_times(self.request_data['start_time'],
                                 self.request_data['end_time'])
        #  Create the course record and insert it.
        self.create_record()
        # Generate response.
        self.response_data.message = SUCCESS.COURSE_CREATED
        self.generate_response()

    # Updates a course record.
    def edit_course(self):
        # Verify valid keys exists in body of JSON request.
        self.verify_request_data(self.valid_keys)
        # Get the record to edit.
        self.get_record_by_id()
        # If there are days, verify the days listed in days are allowed and
        # join list as a comma separated string.
        if 'days' in self.request_data.keys():
            self.verify_days()
        # Conditional checks which time keys are in the reponse data, and
        # uses database record times only one time is in the response data
        if ('start_time' in self.request_data.keys() and 'end_time' in
                self.request_data.keys()):
            # Verify valid times.
            self.verify_time([self.request_data['start_time'],
                              self.request_data['end_time']])
            # Verify times are valid for scheduling
            self.verify_course_times(self.request_data['start_time'],
                                     self.request_data['end_time'])
        elif ('start_time' in self.request_data.keys() and 'end_time' not in
                self.request_data.keys()):
            # Verify valid times.
            self.verify_time([self.request_data['start_time'],
                              self.record.end_time])
            # Verify times are valid for scheduling
            self.verify_course_times(self.request_data['start_time'],
                                     self.record.end_time)
        elif ('start_time' not in self.request_data.keys() and 'end_time' in
                self.request_data.keys()):
            # Verify valid times.
            self.verify_time([self.record.start_time,
                              self.request_data['end_time']])
            # Verify times are valid for scheduling
            self.verify_course_times(self.record.start_time,
                                     self.request_data['end_time'])
        # Build edits to course record and update it.
        self.edit_record()
        # Generate response.
        self.response_data.message = f'{SUCCESS.COURSE_EDITED} {self.uid}'
        self.generate_response()

    # Deletes a course record.
    def delete_course(self):
        self.delete_record()
        self.response_data.message = f'{SUCCESS.COURSE_DELETED} {self.uid}'
        self.generate_response()

    """ COURSE VALIDATION HELPERS
    # ----------------------------------------------------------------------"""
    # Verify that days provided in the request data are valid, and
    # that days are not duplicated.
    def verify_days(self):
        # Verify that provided data is a list.
        if type(self.request_data['days']) is list:
            # Loop through list.
            for day in self.request_data['days']:
                # Verify day in list is valid, error if not.
                if (day.casefold() not in map(
                        str.casefold, SCHEDULE.ALLOWED_DAYS
                        )):
                    raise StatusError(
                        STATUS_ERR.CODE_422,
                        STATUS_ERR.BAD_DAY,
                        422
                    )
                else:
                    # Check for duplicate values, error if duplicates.
                    if self.request_data['days'].count(day) > 1:
                        raise StatusError(
                            STATUS_ERR.CODE_422,
                            STATUS_ERR.DUP_DAY,
                            422
                        )
            self.request_data['days'] = ','.join(self.request_data['days'])
        else:
            raise StatusError(STATUS_ERR.CODE_422, STATUS_ERR.DAY_LIST, 422)

    # Takes validated time string inputs, converts the to integers
    # for comparison, and checks to see that the start time is
    # not after the end time, and that thecourse duration is not
    # too short or too long.
    def verify_course_times(self, start_time, end_time):
        # Convert times to integers.
        start_time = self.time_to_int(start_time)
        end_time = self.time_to_int(end_time)
        # Compare times to validation conditions.
        duration = end_time - start_time
        if (duration < 1 or duration < SCHEDULE.MIN_LENGTH or
                duration > SCHEDULE.MAX_LENGTH or
                start_time < SCHEDULE.MIN_START or
                end_time > SCHEDULE.MAX_END):
            raise StatusError(STATUS_ERR.CODE_422, STATUS_ERR.INV_TIME, 422)


# Controller class for the Assignment databale model.
# -----------------------------------------------------------------------------
class Assignments(Controller):
    # Init self with super.
    def __init__(self, **kwargs):
        super().__init__(table=Assignment, **kwargs)
        # Set valid keys for course record.
        self.valid_keys = ['course_uid', 'instructor_uid']

    # Create an assignment record.
    def create_assignment(self):
        # Verify required keys exist in body of JSON request.
        self.verify_request_data(self.valid_keys, strict=True)
        # Verify IDs are or can be converted to integers
        self.string_to_int(self.request_data['course_uid'])
        self.string_to_int(self.request_data['instructor_uid'])
        # Verify request data, then get records if they exist.
        if (self.request_data['course_uid'] and
                self.request_data['instructor_uid'] > 0):
            course, instructor = self.get_course_and_person(
                Instructor, 'instructor_uid'
            )
        # Verify assignment isn't a duplicate and that there are no
        # schedule conflics.
        self.verify_schedule(course=course, person=instructor.assignments)

        # Create the Assignment record and insert it.
        self.create_record()
        # Generate response.
        self.response_data.message = SUCCESS.ASSIGNMENT_CREATED
        self.generate_response()

    # Deletes an Assignment record.
    def delete_assignment(self):
        self.delete_record()
        self.response_data.message = f'{SUCCESS.ASSIGNMENT_DELETED} {self.uid}'
        self.generate_response()


#  Controller class for the Enrollment databale model.
# -----------------------------------------------------------------------------
class Enrollments(Controller):
    # Init self with super.
    def __init__(self, **kwargs):
        super().__init__(table=Enrollment, **kwargs)
        # Set valid keys for course record.
        self.valid_keys = ['course_uid', 'student_uid']

    # Create an assignment record.
    def create_enrollment(self):
        # Verify required keys exist in body of JSON request.
        self.verify_request_data(self.valid_keys, strict=True)
        # Verify IDs are or can be converted to integers
        self.string_to_int(self.request_data['course_uid'])
        self.string_to_int(self.request_data['student_uid'])
        # Verify request data, then get records if they exist.
        if (self.request_data['course_uid'] and
                self.request_data['student_uid'] > 0):
            course, student = self.get_course_and_person(
                Student, 'student_uid'
            )
        # Verify enrollment isn't a duplicate and that there are no
        # schedule conflics.
        self.verify_schedule(course=course, person=student.enrollments)
        # Create the Assignment record and insert it.
        self.create_record()
        # Generate response.
        self.response_data.message = SUCCESS.ENROLLMENT_CREATED
        self.generate_response()

    # Deletes an Assignment record.
    def delete_enrollment(self):
        self.delete_record()
        self.response_data.message = f'{SUCCESS.ENROLLMENT_DELETED} {self.uid}'
        self.generate_response()
