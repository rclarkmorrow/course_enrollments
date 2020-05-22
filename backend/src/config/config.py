""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


# Dependencies
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

""" --------------------------------------------------------------------------#
# DATABASE SETTINGS
# --------------------------------------------------------------------------"""

# Environmental variables for connecting to database.
db_user = 'postgres'
db_passw = 'postgres'
database_name = 'enrollments'
database_path = ("postgres://{}:{}@{}/{}"
                 .format(db_user, db_passw, 'localhost:5432', database_name))

# Define db
db = SQLAlchemy()


# Bind flask application and SQLAlchemy service
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


""" --------------------------------------------------------------------------#
# Auth0 Settings
# --------------------------------------------------------------------------"""


# TODO: implement Auth0 settings and include settings for bearer tokens


""" --------------------------------------------------------------------------#
# APPLICATION SETTINGS
# --------------------------------------------------------------------------"""

# Set Pagination
PAGINATION_SETTINGS = {
    'STUDENTS_PER_PAGE': 10,
    'INSTRUCTORS_PER_PAGE': 10,
    'COURSES_PER_PAGE': 10
}

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
SCHEDULE_SETTINGS = {
    'ALLOWED_DAYS': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    'MIN_START': 450,  # Default is 7:30 am
    'MAX_END': 990,  # Default is 4:30 pm
    'MIN_LENGTH': 30,  # Default is a half hour.
    'MAX_LENGTH': 150  # Default is two and a half hours.
}
# Enable debug mode.
DEBUG = True
