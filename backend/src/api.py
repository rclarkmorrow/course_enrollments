""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


# Third party dependencies
from flask import Flask, request, jsonify
from flask_cors import CORS

# Local application dependencies
from config.config import setup_db, STATUS_ERR
from controllers.controllers import (Courses, Students, Instructors,
                                     Assignments, Enrollments)
from helpers.helpers import StatusError, get_detail
from auth.auth import requires_auth


""" --------------------------------------------------------------------------#
# CREATE CORS APP, DATABASE, ROUTES AND ERROR HANDLERS
# --------------------------------------------------------------------------"""


def create_app():

    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST, PATCH, DELETE')
        return response

    """------------------------------------------------------------------------#
    # ROUTES
    # -----------------------------------------------------------------------"""

    # Student routes
    # --------------------------------------------------------------------------
    """ View or create students. """
    @app.route('/students', methods=['GET', 'POST'])
    def view_or_manage_students():
        # Respond to GET request.
        if request.method == 'GET':
            @requires_auth('get:students')
            def get_students(jwt):
                # Get detail arguments.
                detail = get_detail()
                page = request.args.get('page')
                # Create Students object.
                this_student_list = Students()
                # Get a list of students with detail.
                this_student_list.list_students(detail=detail, page=page)
                # Return JSON response
                return this_student_list.response
            return get_students()

        # Respond to POST request.
        elif request.method == 'POST':
            @requires_auth('post:student')
            def post_student(jwt):
                # Get response data.
                this_request = request.get_json()
                # Pass response data to controller.
                this_student = Students(request_data=this_request)
                # Create new student.
                this_student.create_student()
                # Return JSON response.
                return this_student.response
            return post_student()

    """ View, edit or delete student by id. """
    @app.route('/students/<uid>', methods=['GET', 'PATCH', 'DELETE'])
    def view_or_manage_student(uid):
        # Get response data.
        this_request = request.get_json()
        # Pass response data and student id to controller.
        this_student = Students(request_data=this_request, uid=uid)
        # Get, patch or delete student and return JSON response.
        if request.method == 'GET':
            @requires_auth('get:student')
            def get_student(jwt):
                this_student.get_student()
            get_student()
        elif request.method == 'PATCH':
            @requires_auth('patch:student')
            def patch_student(jwt):
                this_student.edit_student()
            patch_student()
        elif request.method == "DELETE":
            @requires_auth('delete:student')
            def delete_student(jwt):
                this_student.delete_student()
            delete_student()
        # Return JSON response.
        return this_student.response

    """ Get courses student is enrolled in. """
    @app.route('/students/<uid>/courses', methods=['GET'])
    @requires_auth('get:student-courses')
    def view_student_with_courses(payload, uid):
        # Create Students object.
        this_student = Students(uid=uid)
        # Get a list of courses with students detail.
        this_student.get_student_with_courses()
        # Return JSON response.
        return this_student.response

    # Instructor routes
    # -------------------------------------------------------------------------
    """ View or create instructors. """
    @app.route('/instructors', methods=['GET', 'POST'])
    def view_or_manage_instsructors():
        # Respond to GET request.
        if request.method == 'GET':
            @requires_auth('get:instructors')
            def get_instructors(jwt):
                # Get detail arguments.
                detail = get_detail()
                page = request.args.get('page')
                # Create Instructors object.
                this_instructor_list = Instructors()
                # Get a list of instructors with detail.
                this_instructor_list.list_instructors(detail=detail, page=page)
                # Return JSON response
                return this_instructor_list.response
            return get_instructors()
        # Respond to POST request.
        elif request.method == 'POST':
            @requires_auth('post:instructor')
            def post_instructor(jwt):
                # Get response data.
                this_request = request.get_json()
                # Pass response data to controller.
                this_instructor = Instructors(request_data=this_request)
                # Create new instructor.
                this_instructor.create_instructor()
                # Return JSON response.
                return this_instructor.response
            return post_instructor()

    """ View, edit or delete instructor by id. """
    @app.route('/instructors/<uid>', methods=['GET', 'PATCH', 'DELETE'])
    def view_or_manage_instructor(uid):
        # Get response data.
        this_request = request.get_json()
        # Pass response data and instructor id to controller.
        this_instructor = Instructors(request_data=this_request, uid=uid)
        # Get, patch or delete instructor and return JSON response.
        if request.method == 'GET':
            @requires_auth('get:instructor')
            def get_instructor(jwt):
                this_instructor.get_instructor()
            get_instructor()
        elif request.method == 'PATCH':
            @requires_auth('patch:instructor')
            def patch_instructor(jwt):
                this_instructor.edit_instructor()
            patch_instructor()
        elif request.method == "DELETE":
            @requires_auth('delete:instructor')
            def delete_instructor(jwt):
                this_instructor.delete_instructor()
            delete_instructor()
        # Return JSON response.
        return this_instructor.response

    """ Get courses instructor is assigned to. """
    @app.route('/instructors/<uid>/courses', methods=['GET'])
    @requires_auth('get:instructor-courses')
    def view_instructor_courses(payload, uid):
        # Create Students object.
        this_instructor = Instructors(uid=uid)
        # Get a list of courses with students detail.
        this_instructor.get_instructor_with_courses()
        # Return JSON response
        return this_instructor.response

    # Course routes
    # -------------------------------------------------------------------------
    """ View or create courses. """
    @app.route('/courses', methods=['GET', 'POST'])
    def view_or_manage_courses():
        # Respond to GET request.
        if request.method == 'GET':
            # Get detail arguments.
            detail = get_detail()
            page = request.args.get('page')
            # Create Courses object.
            this_course_list = Courses()
            # Get a list of courses with detail.
            this_course_list.list_courses(detail=detail, page=page)
            # Return JSON response
            return this_course_list.response
        # Respond to POST request.
        elif request.method == 'POST':
            @requires_auth('post:course')
            def post_course(jwt):
                # Get response data.
                this_request = request.get_json()
                # Pass response data to controller.
                this_course = Courses(request_data=this_request)
                # Create new course.
                this_course.create_course()
                # Return JSON response.
                return this_course.response
            return post_course()

    """ View, edit or delete a course by id. """
    @app.route('/courses/<uid>', methods=['GET', 'PATCH', 'DELETE'])
    def view_or_manage_course(uid):
        # Get response data.
        this_request = request.get_json()
        # Pass response data and course id to controller.
        this_course = Courses(request_data=this_request, uid=uid)
        # Get, patch or delete course and return JSON response.
        if request.method == 'GET':
            this_course.get_course()
        elif request.method == 'PATCH':
            @requires_auth('patch:course')
            def patch_course(jwt):
                this_course.edit_course()
            patch_course()
        elif request.method == "DELETE":
            @requires_auth('delete:course')
            def delete_course(jwt):
                this_course.delete_course()
            delete_course()
        # Return JSON response.
        return this_course.response

    """ Get students enrolled in a course. """
    @app.route('/courses/<uid>/students', methods=['GET'])
    @requires_auth('get:course-students')
    def view_students_enrolled(payload, uid):
        # Create Courses object.
        this_course = Courses(uid=uid)
        # Get a list of courses with students detail.
        this_course.get_course_with_students()
        # Return JSON response.
        return this_course.response

    """ Get instructors assigned to a a course. """
    @app.route('/courses/<uid>/instructors', methods=['GET'])
    @requires_auth('get:course-instructors')
    def view_instructors_assigned(payload, uid):
        # Create Courses object.
        this_course = Courses(uid=uid)
        # Get a list of courses with instructors detail.
        this_course.get_course_with_instructors()
        # Return JSON response.
        return this_course.response

    # Assignment routes
    # -------------------------------------------------------------------------
    """ Create an assignment. """
    @app.route('/assignments', methods=['POST'])
    @requires_auth('post:assignment')
    def assign_course(payload):
        # Get response data.
        this_request = request.get_json()
        # Pass response data to controller.
        this_assignment = Assignments(request_data=this_request)
        # Create new assignment.
        this_assignment.create_assignment()
        # Return JSON response.
        return this_assignment.response

    """ Delete an Assignment. """
    @app.route('/assignments/<uid>', methods=['DELETE'])
    @requires_auth('delete:assignment')
    def delete_assignment(payload, uid):
        # Pass  the enrollment id to controller.
        this_assignment = Assignments(uid=uid)
        # Delete the course.
        this_assignment.delete_assignment()
        # Return JSON response.
        return this_assignment.response

    # Enrollment routes
    # -------------------------------------------------------------------------
    """ Create an enrollment. """
    @app.route('/enrollments', methods=['POST'])
    @requires_auth('post:enrollment')
    def enroll_course(payload):
        # Get response data.
        this_request = request.get_json()
        # Pass response data to controller.
        this_enrollment = Enrollments(request_data=this_request)
        # Create new enrollment.
        this_enrollment.create_enrollment()
        # Return JSON response.
        return this_enrollment.response

    """ Delete an enrollment. """
    @app.route('/enrollments/<uid>', methods=['DELETE'])
    @requires_auth('delete:enrollment')
    def delete_enrollment(payload, uid):
        # Pass  the enrollment id to controller.
        this_enrollment = Enrollments(uid=uid)
        # Delete the course.
        this_enrollment.delete_enrollment()
        # Return JSON response.
        return this_enrollment.response

    """ ----------------------------------------------------------------------#
    # ERROR_HANDLING
    # ----------------------------------------------------------------------"""

    # Handles errors passed by the StatusError function.
    @app.errorhandler(StatusError)
    def status_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.message,
            'description': error.description
        }), error.status_code

    # Handles unspecified 400 errors.
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': STATUS_ERR.CODE_400
        }), 400

    # Handles unspecified 404 errors.
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': STATUS_ERR.CODE_404
        }), 404

    # Handles unspecified 405 errors.
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': STATUS_ERR.CODE_405
        }), 405

    # Handles unspecified 422 errors.
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': STATUS_ERR.CODE_422
        }), 422

    # Handles unspecified 500 errors.
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'succes': False,
            'error': 500,
            'message': STATUS_ERR.CODE_500
        }), 500

    return app
