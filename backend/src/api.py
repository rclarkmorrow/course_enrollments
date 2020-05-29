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
            # Get detail arguments.
            detail = get_detail()
            page = request.args.get('page')
            # Create Students object.
            this_student_list = Students()
            # Get a list of students with detail.
            this_student_list.list_students(detail=detail, page=page)
            # Return JSON response
            return this_student_list.response
        # Respond to POST request.
        elif request.method == 'POST':
            # Get response data.
            this_request = request.get_json()
            # Pass response data to controller.
            this_student = Students(request_data=this_request)
            # Create new student.
            this_student.create_student()
            # Return JSON response.
            return this_student.response

    """ View, edit or delete student by id. """
    @app.route('/students/<uid>', methods=['GET', 'PATCH', 'DELETE'])
    def view_or_manage_student(uid):
        # Get response data.
        this_request = request.get_json()
        # Pass response data and student id to controller.
        this_student = Students(request_data=this_request, uid=uid)
        # Get, patch or delete student and return JSON response.
        if request.method == 'GET':
            this_student.get_student()
        elif request.method == 'PATCH':
            this_student.edit_student()
        elif request.method == "DELETE":
            this_student.delete_student()
        # Return JSON response.
        return this_student.response

    """ Get courses student is enrolled in. """
    @app.route('/students/<uid>/courses', methods=['GET'])
    def view_student_with_courses(uid):
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
            # Get detail arguments.
            detail = get_detail()
            page = request.args.get('page')
            # Create Instructors object.
            this_instructor_list = Instructors()
            # Get a list of instructors with detail.
            this_instructor_list.list_instructors(detail=detail, page=page)
            # Return JSON response
            return this_instructor_list.response
        # Respond to POST request.
        elif request.method == 'POST':
            # Get response data.
            this_request = request.get_json()
            # Pass response data to controller.
            this_instructor = Instructors(request_data=this_request)
            # Create new instructor.
            this_instructor.create_instructor()
            # Return JSON response.
            return this_instructor.response

    """ View, edit or delete instructor by id. """
    @app.route('/instructors/<uid>', methods=['GET', 'PATCH', 'DELETE'])
    def view_or_manage_instructor(uid):
        # Get response data.
        this_request = request.get_json()
        # Pass response data and instructor id to controller.
        this_instructor = Instructors(request_data=this_request, uid=uid)
        # Get, patch or delete instructor and return JSON response.
        if request.method == 'GET':
            this_instructor.get_instructor()
        elif request.method == 'PATCH':
            this_instructor.edit_instructor()
        elif request.method == "DELETE":
            this_instructor.delete_instructor()
        # Return JSON response.
        return this_instructor.response

    """ Get courses instructor is assigned to. """
    @app.route('/instructors/<uid>/courses', methods=['GET'])
    def view_instructor_courses(uid):
        # Create Students object.
        this_student = Instructors(uid=uid)
        # Get a list of courses with students detail.
        this_student.get_instructor_with_courses()
        # Return JSON response
        return this_student.response

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
            # Get response data.
            this_request = request.get_json()
            # Pass response data to controller.
            this_course = Courses(request_data=this_request)
            # Create new course.
            this_course.create_course()
            # Return JSON response.
            return this_course.response

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
            this_course.edit_course()
        elif request.method == "DELETE":
            this_course.delete_course()
        # Return JSON response.
        return this_course.response

    """ Get students enrolled in a course. """
    @app.route('/courses/<uid>/students', methods=['GET'])
    def view_students_enrolled(uid):
        # Create Courses object.
        this_course = Courses(uid=uid)
        # Get a list of courses with students detail.
        this_course.get_course_with_students()
        # Return JSON response.
        return this_course.response

    """ Get instructors assigned to a a course. """
    @app.route('/courses/<uid>/instructors', methods=['GET'])
    def view_instructors_assigned(uid):
        # Create Courses object.
        this_course = Courses(uid=uid)
        # Get a list of courses with instructors detaildetail.
        this_course.get_course_with_instructors()
        # Return JSON response.
        return this_course.response

    # Assignment routes
    # -------------------------------------------------------------------------
    """ Create an assignment. """
    @app.route('/assignments', methods=['POST'])
    def assign_course():
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
    def delete_assignment(uid):
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
    def enroll_course():
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
    def delete_enrollment(uid):
        # Pass  the enrollment id to controller.
        this_enrollment = Enrollments(uid=uid)
        # Delete the course.
        this_enrollment.delete_enrollment()
        # Return JSON response.
        return this_enrollment.response

    """ ----------------------------------------------------------------------#
    # ERROR_HANDLING
    # ----------------------------------------------------------------------"""

    """ NOTE: Uncomment when auth0 implemented """
    # @app.errorhandler(AuthError)
    # def auth_error(error):
    #     return jsonify({
    #         'success': False,
    #         'error': error.status_code,
    #         'message': error.error
    #     }), error.status_code

    @app.errorhandler(StatusError)
    def status_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.message,
            'description': error.description
        }), error.status_code

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': STATUS_ERR.CODE_400
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': STATUS_ERR.CODE_404
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': STATUS_ERR.CODE_405
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': STATUS_ERR.CODE_422
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'succes': False,
            'error': 500,
            'message': STATUS_ERR.CODE_500
        }), 500

    return app
