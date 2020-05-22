""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


# Dependencies
import json  # NOTE: Remove if not used.
import re
from flask import jsonify, abort
from types import SimpleNamespace

# Local modules
from ..database.models import (Student, Instructor, Course,
                               Assignment, Enrollment)
from ..config.config import (SCHEDULE_SETTINGS)


""" --------------------------------------------------------------------------#
# CONTROLLER CLASSES
# --------------------------------------------------------------------------"""


# A super class that initialises data commonly used by the different
# controller classes and contains commonly used methods.
class Controller:
    # Init self with data
    def __init__(self, table=None, request_data=None, uid=None):
        self.request_data = request_data
        print(request_data)
        self.table = table
        self.uid = uid
        if uid:   # When uid is not one, convert to integer.
            self.uid = self.string_to_int(uid)
        self.response_data = SimpleNamespace(success=True)
        self.status = SimpleNamespace(error=False)

    # Generates JSON response.
    def generate_response(self):
        self.response = jsonify(self.response_data.__dict__), 200

    # Converts a uid passed as a string to an integer value, returns
    # an HTTP error if it is not possible.
    def string_to_int(self, int_string):
        if (type(int_string)) != int:
            try:
                int_string = int(int_string)
                return int_string
            except ValueError:
                abort(422)

    # Converts a time string to an integer value expressed as minutes.
    def time_to_int(self, time_string):
        try:
            time_int = (int(time_string[:2]) * 60) + int(time_string[3:])
        except ValueError:
            abort(422)
        return time_int

    # Verify that a string representing a time is valid 24-hour time
    # and raise an HTTP error if not.
    def verify_time(self, time_string):
        if not re.search(
                r'^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$', time_string
                ):
            print('NOT!!!')
            abort(422)

    # Verify request data is valid.
    def verify_request_data(self, valid_keys, strict=False):
        # Verifies that all valid keys are present in the
        # request body.
        if strict is True:
            for data in valid_keys:
                if data not in self.request_data.keys():
                    abort(422)
        # Verifies that there are no invalid keys present
        # in the request body.        
        for key in self.request_data.keys():
            if key not in valid_keys:
                abort(422)

    # Verify the days listed in days are allowed and join list as
    # a comma separated string.
    def verify_days(self):
        # Verify that days 
        if type(self.request_data['days']) is list:
            for day in self.request_data['days']:
                print('day: ', day)
                if (day.casefold() not in map(
                        str.casefold, SCHEDULE_SETTINGS['ALLOWED_DAYS']
                        )):
                    abort(422)
            self.request_data['days'] = ','.join(self.request_data['days'])
        else:
            abort(404)

    # Adds records to class object with argument that determines
    # whether the records have full details or truncated details.
    def append_records_list(self, table=None, detail='full'):
        # Get all records as a query object.
        query = self.get_all_records()
        # Structure details
        if detail == 'full':
            self.records = [record.full() for record in query]
        elif detail == 'short':
            self.records = [record.short() for record in query]
        else:
            abort(422)

    # Builds a new record and inserts in the database.
    def create_record(self):
        self.record = self.table()
        for key, value in self.request_data.items():
            setattr(self.record, key, value)
        self.record.insert()

    def edit_record(self):
        for key, value in self.request_data.items():
            setattr(self.record, key, value)
        self.record.update()

    # Gets record by ID and deletes it.
    def delete_record(self):
        self.get_record_by_id()
        print('this record :', self.record)
        self.record.delete()

    # Get all records from provided table.
    def get_all_records(self):
        if self.table:
            return self.table.query.all()
        else:
            abort(422)

    # Get a single record by provided table.
    def get_record_by_id(self):
        print('Get by ID init')
        if self.table:
            self.record = (self.table.query
                           .filter(self.table.uid == self.uid).first())
            if not self.record:
                abort(404)
        else:
            abort(422)


# Controller for the Student database model.
class Students(Controller):
    # Init self with super.
    def __init__self(self, **kwargs):
        super().__init__(table=Student, **kwargs)


# Controller for the Instructor database model.
class Instructors(Controller):
    # Init self with super.
    def __init__self(self, **kwargs):
        super().__init__(table=Instructor, **kwargs)


# Controller for the Course database model.
class Courses(Controller):
    # Init self with super.
    def __init__(self, **kwargs):
        super().__init__(table=Course, **kwargs)
        # Set valid keys for course record.
        self.valid_keys = ['title', 'days', 'description',
                           'start_time', 'end_time']

    # Returns a list of courses.
    def list_courses(self, detail='full'):
        self.append_records_list(detail=detail)
        self.response_data.courses = self.records
        self.generate_response()

    # Creates a new course record.
    def create_course(self):
        # Verify required keys exist in body of JSON request.
        self.verify_request_data(self.valid_keys, strict=True)
        # Verify valid days.
        self.verify_days()
        # NOTE: Basic time validation methods, need to see 
        # if a common method can work for both creation and editing.
        self.verify_time(self.request_data['start_time'])
        self.verify_time(self.request_data['end_time'])
        start_time = self.string_to_int('start_time')
        end_time = self.time_to_int('end_time')
        duration = end_time - start_time
        if (duration < 1 or duration < SCHEDULE_SETTINGS['MIN_LENGTH'] or
                duration > SCHEDULE_SETTINGS['MAX_LENGTH'] or 
                start_time < SCHEDULE_SETTINGS['MIN_START'] or
                end_time > SCHEDULE_SETTINGS['MAX_END']):
            abort(422)

        #  Create the course record and insert it.
        self.create_record()
        # Generate response.
        self.response_data.message = 'course created'
        self.generate_response()

    def edit_course(self):
        # Verify valid keys exists in body of JSON request.
        self.verify_request_data(self.valid_keys)
        # Get the record to edit.
        self.get_record_by_id()
        # Verify valid start and end times.
        if ('start_time' in self.request_data.keys() or 'end_time' in
                self.request_data.keys()):
            self.verify_time(self.request_data['start_time'])
            self.verify_time(self.request_data['end_time'])
            start_time = self.string_to_int('start_time')
            end_time = self.time_to_int('end_time')
            duration = end_time - start_time
            if (duration < 1 or duration < SCHEDULE_SETTINGS['MIN_LENGTH'] or
                    duration > SCHEDULE_SETTINGS['MAX_LENGTH'] or 
                    start_time < SCHEDULE_SETTINGS['MIN_START'] or
                    end_time > SCHEDULE_SETTINGS['MAX_END']):
                abort(422)
                
            # NOTE: This won't work; there could be a scenario where only a new start
            #       time or a new end time is entered, and will require comparisons
            #       to the record as well.

        # If there are days, verify the days listed in days are allowed and
        # join list as a comma separated string.
        if 'days' in self.request_data.keys():
            self.verify_days()
        # Build edits to course record and update it.
        self.edit_record()
        # Generate response.
        self.response_data.message = f'updated course with id: {self.uid}'
        self.generate_response()

    def delete_course(self):
        self.delete_record()
        self.response_data.message = f'deleted course with id: {self.uid}'
        self.generate_response()

    # TEST METHOD
    def verify_times(self):
        TEST_1 = "12:59"
        TEST_2 = "13:30"

        first = self.time_to_int(TEST_1)
        second = self.time_to_int(TEST_2)
        duration = second - first
        print(f'First: {first} | Second: {second}')
        print(f'Diff: {first - second}')

        if (duration < 1 or 
                duration < SCHEDULE_SETTINGS['MIN_LENGTH'] or
                first < SCHEDULE_SETTINGS['MIN_START'] or
                second > SCHEDULE_SETTINGS['MAX_START']):
            abort(422)