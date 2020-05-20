""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


# Dependencies
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


""" --------------------------------------------------------------------------#
# DATABASE
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
# SETTINGS
# --------------------------------------------------------------------------"""


# Enable debug mode.
DEBUG = True
