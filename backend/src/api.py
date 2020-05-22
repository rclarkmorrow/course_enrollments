""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


# Dependencies
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from random import randint  # @TODO: Remove when not needed.

# Local modules
from .config.config import setup_db
from .database.models import (Student, Instructor, Course, Assignment,
                              Enrollment)
from .controllers.controllers import (Courses)


""" --------------------------------------------------------------------------#
# CREATE CORS APP AND DATABASE
# --------------------------------------------------------------------------"""

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


""" --------------------------------------------------------------------------#
# Routes
# --------------------------------------------------------------------------"""


# Student routes
# -----------------------------------------------------------------------------
""" @TODO: implement student routes """


@app.route('/students', methods=['GET', 'POST'])
def view_or_create_students():
   return jsonify({
            'success': False,
            'message': 'not implemented'
        }), 501


# Instructor routes
# -----------------------------------------------------------------------------
""" @TODO: implement instructor routes """


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
            bio='Jane Aweomse is an expert on basket weaving and is awesome.'
        )
        this_instructor.insert()
        return jsonify({
                'success': 'true',
                'message': 'instructor created'
        }), 200


# Course routes
# -----------------------------------------------------------------------------
@app.route('/courses', methods=['GET', 'POST'])
def view_or_manage_courses():
    # Respond to GET request.
    if request.method == 'GET':
        # Create Courses object and create list of all courses.
        detail = request.args.get('detail')
        if not detail:
            detail = 'full'
        # Validate argument.
        if detail != 'short' and detail != 'full':
            abort(422)
        # Get course list with detail.
        this_course_list = Courses()
        this_course_list.list_courses(detail=detail)
        # Return JSON response
        return this_course_list.response
    # Respond to POST request.
    elif request.method == 'POST':
        this_request = request.get_json()
        this_course = Courses(request_data=this_request)
        this_course.create_course()
        # Return JSON response.
        return this_course.response
    else:
        abort(422)

# @TODO: COMMENTS!!
@app.route('/courses/<uid>', methods=['GET', 'PATCH', 'DELETE'])
def view_or_manage_course(uid):
    this_request = request.get_json()
    this_course = Courses(request_data=this_request, uid=uid)
    if request.method == 'GET':
        return jsonify({
            'success': False,
            'message': 'not implemented'
        }), 501
    elif request.method == 'PATCH':
        this_course.edit_course()
        return this_course.response
    elif request.method == "DELETE":
        this_course.delete_course()
        return this_course.response
    else:
        abort(422)


@app.route('/courses/<uid>/students', methods=['GET'])
def view_students_enrolled():
    return jsonify({
                'success': False,
                'message': 'not implemented'
            }), 501


@app.route('/courses/<uid>/instructors', methods=['GET'])
def view_instructors_assigned():
    return jsonify({
        'success': False,
        'message': 'not implemented'
    }), 501


# Assignment routes
# -----------------------------------------------------------------------------
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
                'message': 'course created'
        }), 200


@app.route('assignment/<uid>', methods=['DELETE'])
def delete_assignment():
    return jsonify({
        'success': False,
        'message': 'not implemented'
    }), 501


# Enrollment routes
# -----------------------------------------------------------------------------
@app.route('/assignment', methods=['POST'])
def enroll_course():
    return jsonify({
        'success': False,
        'message': 'not implemented'
    }), 501


@app.route('assignment/<uid>', methods=['DELETE'])
def delete_enrollment():
    return jsonify({
        'success': False,
        'message': 'not implemented'
    }), 501

""" --------------------------------------------------------------------------#
# ERROR_HANDLING
# --------------------------------------------------------------------------"""

#NOTE: Uncomment when auth0 implemented
# @app.errorhandler(AuthError)
# def auth_error(error):
#     return jsonify({
#         'success': False,
#         'error': error.status_code,
#         'message': error.error
#     }), error.status_code

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'bad request'
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'succes': False,
        'error': 500,
        'message': 'internal server error'
    }), 500
