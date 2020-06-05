""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""

# Standard Library dependencies
import os
from types import SimpleNamespace

# Third party dependencies
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


""" --------------------------------------------------------------------------#
# DATABASE SETTINGS
# --------------------------------------------------------------------------"""


# Environmental variables for connecting to a local PSQL database.
# NOTE: If running locally, replace information with local
# environmental variables.
db_user = 'postgres'
db_passw = 'postgres'
database_name = 'enrollments'
database_host = 'localhost:5432'
database_path = ("postgresql://{}:{}@{}/{}"
                 .format(db_user, db_passw, database_host, database_name))


# Returns alternate path for local test database.
# NOTE: If running locally, replace information with local
# environmental variables.
def create_test_db_path():
    db_user = 'postgres'
    db_passw = 'postgres'
    database_name = 'test-enrollments'
    database_host = 'localhost:5432'
    database_path = ("postgresql://{}:{}@{}/{}"
                     .format(db_user, db_passw, database_host,
                             database_name))
    return database_path


# Environmental variable for DB paths.
database_path = os.getenv('DATABASE_URL', database_path)
test_database_path = os.getenv('HEROKU_POSTGRESQL_COPPER_URL',
                               create_test_db_path())

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


""" --------------------------------------------------------------------------#
# AUTH0 SETTINGS
# --------------------------------------------------------------------------"""


# Default Auth0 environmental variables.
# NOTE: If creating your own deployment, these should be
# updated with your auth0 account details. 
DOMAIN = 'rclarkmorrow.auth0.com'
ALGORITHMS = 'RS256'
API_AUDIENCE = 'course-enrollments-services'
CLIENT_ID = 'vsWulCF5Hcv5iFzlSQLxKuzSAcApam2c'
CLIENT_SECRET = ('IcouX6edbuTSuYEz8F2iwEfyjuJefnKckv6eD'
                 'oQLjRAMluvDJjehIbSHLxBiwaVg')


# Auth0 variables oject.
AUTH0 = SimpleNamespace(
    DOMAIN=os.getenv('DOMAIN', DOMAIN),
    ALGORITHMS=os.getenv('ALGORITHMS', ALGORITHMS),
    API_AUDIENCE=os.getenv('API_AUDIENCE', API_AUDIENCE),
    CLIENT_ID=os.getenv('CLIENT_ID', CLIENT_ID),
    CLIENT_SECRET=os.getenv('CLIENT_SECRET', CLIENT_SECRET)
)

# Default test users.
# NOTE: If creating your own deployment, these should be
# updated with your specific test user details.
DEAN = SimpleNamespace(
    NAME='dean@rclarkmorrow.com',
    PASSWORD='TestDean1'
)
REGISTRAR = SimpleNamespace(
    NAME='registrar@rclarkmorrow.com',
    PASSWORD='TestRegistrar1'
)
INSTRUCTOR = SimpleNamespace(
    NAME='instructor@rclarkmorrow.com',
    PASSWORD='TestInstructor1'
)


# Test user variables object.
TEST_USERS = SimpleNamespace(
    DEAN=SimpleNamespace(
        NAME=os.getenv('DEAN_NAME', DEAN.NAME),
        PASSWORD=os.getenv('DEAN_PASSWORD', DEAN.PASSWORD)
    ),
    REGISTRAR=SimpleNamespace(
        NAME=os.getenv('REGISTRAR_NAME', REGISTRAR.NAME),
        PASSWORD=os.getenv('REGISTRAR_PASSWORD', REGISTRAR.PASSWORD)
    ),
    INSTRUCTOR=SimpleNamespace(
        NAME=os.getenv('INSTRUCTOR_NAME', INSTRUCTOR.NAME),
        PASSWORD=os.getenv('INSTRUCTOR_PASSWORD', INSTRUCTOR.PASSWORD)
    )
)


""" --------------------------------------------------------------------------#
# APPLICATION SETTINGS
# --------------------------------------------------------------------------"""


# Enable debug mode.
DEBUG = False

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
