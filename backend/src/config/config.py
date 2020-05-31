""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""

# Standard Library dependencies
from types import SimpleNamespace

# Third party dependencies
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


""" --------------------------------------------------------------------------#
# DATABASE SETTINGS
# --------------------------------------------------------------------------"""


# Environmental variables for connecting to database.
db_user = 'postgres'
db_passw = 'postgres'
database_name = 'enrollments'
database_path = ("postgresql://{}:{}@{}/{}"
                 .format(db_user, db_passw, 'localhost:5432', database_name))

# Define db
db = SQLAlchemy()


# Bind flask application and SQLAlchemy service
def setup_db(app, db_path=None):
    if not db_path:
        db_path = database_path
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


# Returns alternate path for test database:
def create_test_db_path():
    db_user = 'postgres'
    db_passw = 'postgres'
    database_name = 'test-enrollments'
    database_path = ("postgresql://{}:{}@{}/{}"
                     .format(db_user, db_passw, 'localhost:5432',
                             database_name))
    return database_path


""" --------------------------------------------------------------------------#
# AUTH0 SETTINGS
# --------------------------------------------------------------------------"""


AUTH0 = SimpleNamespace(
    DOMAIN='rclarkmorrow.auth0.com',
    ALGORITHMS=['RS256'],
    API_AUDIENCE='course-enrollments-services'
)


""" --------------------------------------------------------------------------#
# APPLICATION SETTINGS
# --------------------------------------------------------------------------"""


# Enable debug mode.
DEBUG = True

# Regex expressions for validation.
REGEX = SimpleNamespace(
    PHONE_ONE=r'^[0-9]{3}-[0-9]{3}-[0-9]{4}$',
    PHONE_TWO=r'^[0-9]{10}$',
    EMAIL=(r'^[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]'
           r'+\.)+[a-zA-Z]{2,7}$')
)

# Set Pagination
PAGE_LENGTH = SimpleNamespace(
    STUDENTS=10,
    INSTRUCTORS=10,
    COURSES=10
)

""" Set allowed scheduling:
    NOTE: Allowed days is a list of days that courses can be scheduled on, a
          course can occurr in a timeslot on multiple days.
    NOTE: Time values are assumed to be 24 Hour time and are represented as
          integers calculated as [(hour * 60) + minutes]. For example 14:30
          (2:30pm) is 870. The value MUST be between 0 (midnight) and 1439
          (11:59pm):
            - Min start time is the earlist a course can start on a day.
            - Max start time is the lastest a course can start on a day.
    NOTE: Time length values a duration expressed in total minutes:
            - Min length is the shortest a course can be scheduled for.
            - Max length is the longes ta course can be schedules for.
"""
SCHEDULE = SimpleNamespace(
    ALLOWED_DAYS=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    MIN_START=450,  # Default is 7:30 am
    MAX_END=990,  # Default is 4:30 pm
    MIN_LENGTH=30,  # Default is a half hour.
    MAX_LENGTH=150  # Default is two and a half hours.
)


""" --------------------------------------------------------------------------#
# MESSAGES
# --------------------------------------------------------------------------"""

# Success messages
# -----------------------------------------------------------------------------

SUCCESS = SimpleNamespace(
    COURSE_CREATED='course created',
    COURSE_EDITED='updated course with uid:',
    COURSE_DELETED='deleted course with uid:',
    STUDENT_CREATED='student created',
    STUDENT_EDITED='updated student with uid:',
    STUDENT_DELETED='deleted student with uid:',
    INSTRUCTOR_CREATED='instructor created',
    INSTRUCTOR_EDITED='updated instructor with uid:',
    INSTRUCTOR_DELETED='deleted instructor with uid:',
    ASSIGNMENT_CREATED='assignment created',
    ASSIGNMENT_DELETED='deleted assignment with uid:',
    ENROLLMENT_CREATED='enrollment created',
    ENROLLMENT_DELETED='deleted enrollment with uid:'
)

STATUS_ERR = SimpleNamespace(
    # Status Code Messages
    CODE_400='bad request',
    CODE_401='unauthorized',
    CODE_404='resource not found',
    CODE_405='method not allowed',
    CODE_422='request unprocessable',
    CODE_500='internal server error',
    # Additional error descriptions.
    GENERIC='request could not be processed due to an error',
    BAD_DETAIL=('detail must be full or short, defaults to full with no'
                ' arguments'),
    BAD_INT='value could not be converted to integer',
    BAD_TIME=('you must use 24-Hour time as a string in the format: HH:MM'),
    MISSING_KEY='at least one required key is missing from the request body',
    BAD_KEY='the request body contains at least one invalid key',
    BAD_DAY='the request body contains at least on invalid day',
    DUP_DAY='duplicate days are not allowed',
    DAY_LIST='scheduled days must be provided in list format',
    INV_TIME='the request body contains at least one invalid time',
    NO_RECORD='one or more provided uids not found in database',
    NO_RECORDS='no records found in database.',
    BAD_PAGE='the page argument must be an integer above zero.',
    BAD_PHONE='phone numbers must be in formats: 1234567890 or 123-456-7890',
    BAD_EMAIL='the email provided is invalid.',
    UNIQUE_GENERIC='at least one key needs to be a unique value',
    UNIQUE_EMAIL='email must be a unique value',
    BAD_ID='uids must be provided as integers',
    CONFLICT='a course is arleady scheduled for this time',
    DUPLICATE='a matching record already exists',
    # Authorization error descriptions.
    HEADER_MISSING='authorization header expected',
    BEARER_MISSING='authorization header must start with bearer',
    TOKEN_MISSING='token not found',
    BEARER_TOKEN='authorization header must be bearer token',
    PERMISSIONS_MISSING='permissions not included in payload',
    NOT_AUTHORIZED='token not authorized for this request',
    TOKEN_EXPIRED='this token has expired',
    INV_CLAIMS='incorrect claims, please check the audience and issuer',
    PARSE_TOKEN='unable to parse authentication token',
    KEY_FIND='unable to find appropriate key'
)
