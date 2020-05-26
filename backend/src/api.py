""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


# Standard library dependencies
from random import randint  # @TODO: Remove when not needed.

# Third party dependencies
from flask import Flask, request, jsonify
from flask_cors import CORS

# Local application dependencies
from config.config import setup_db, STATUS_ERR
from database.models import (Instructor, Assignment, Enrollment)
from controllers.controllers import (Courses, Students)
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
            this_course = Students(request_data=this_request)
            # Create new student.
            this_course.create_student()
            # Return JSON response.
            return this_course.response

    """ View, edit or delete student by id. """
    @app.route('/students/<uid>', methods=['GET', 'PATCH', 'DELETE'])
    def view_or_manage_student(uid):
        # Get response data.
        this_request = request.get_json()
        # Pass response data and student id to controller.
        this_student = Students(request_data=this_request, uid=uid)
        # Get, patch or delete course and return JSON response.
        if request.method == 'GET':
            this_student.get_student()
        elif request.method == 'PATCH':
            this_student.edit_student()
        elif request.method == "DELETE":
            this_student.delete_student()
        return this_student.response

    """ Get courses student is enrolled in. """
    @app.route('/student/<uid>/coruses', methods=['GET'])
    def view_student_courses():
        return jsonify({
                    'success': False,
                    'message': 'not implemented'
                }), 501

    # Instructor routes - TODO: Finish Routes
    # -------------------------------------------------------------------------
    """ TODO: Finish Implementing Routes"""
    @app.route('/instructors', methods=['GET', 'POST', 'DELETE'])
    def view_or_manage_instructors():
        # Respond to GET request.
        """ @TODO: implement show instructor list """

        # Test case for adding instructor.
        if request.method == 'POST':
            rand = randint(0, 5000)

            this_instructor = Instructor(
                name='Jane Awesome',
                email=f'jane_awesome{rand}@university.edu',
                phone='123-555-0808',
                bio='Jane Aweomse is an expert on basket weaving and is awes.'
            )
            this_instructor.insert()
            return jsonify({
                    'success': 'true',
                    'message': 'instructor created'
            }), 200

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
        return this_course.response

    """ Get students enrolled in a course. """
    @app.route('/courses/<uid>/students', methods=['GET'])
    def view_students_enrolled():
        return jsonify({
                    'success': False,
                    'message': 'not implemented'
                }), 501

    """ Get instructors assigned to a a course. """
    @app.route('/courses/<uid>/instructors', methods=['GET'])
    def view_instructors_assigned():
        return jsonify({
            'success': False,
            'message': 'not implemented'
        }), 501

    # Assignment routes
    # -------------------------------------------------------------------------
    @app.route('/assignment', methods=['POST'])
    def assign_course():
        # TEST CASE
        if request.method == 'POST':
            this_assignment = Assignment(
                course_uid=1,
                instructor_uid=3,
            )
            this_assignment.insert()
            return jsonify({
                    'success': 'true',
                    'message': 'assignment created'
            }), 200

    @app.route('/assignment/<uid>', methods=['DELETE'])
    def delete_assignment():
        return jsonify({
            'success': False,
            'message': 'not implemented'
        }), 501

    # Enrollment routes
    # -------------------------------------------------------------------------
    @app.route('/enrollment', methods=['POST'])
    def enroll_course():
        # TEST CASE
        if request.method == 'POST':
            this_enrollment = Enrollment(
                course_uid=1,
                student_uid=3,
            )
            this_enrollment.insert()
            return jsonify({
                    'success': 'true',
                    'message': 'assignment created'
            }), 200

    @app.route('/enrollment/<uid>', methods=['DELETE'])
    def delete_enrollment():
        return jsonify({
            'success': False,
            'message': 'not implemented'
        }), 501

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
