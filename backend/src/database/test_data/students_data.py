""" ---------------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------------"""


# Standard library dependencies
from types import SimpleNamespace

# Local application dependencies
from database.models import Student


""" ---------------------------------------------------------------------------
# TEST DATA CLASS
# --------------------------------------------------------------------------"""


# Class initializes with test data, and methods to populate test database.
# -----------------------------------------------------------------------------
class StudentTest:
    def __init__(self):
        # Seed data for test database
        self.seeds = [
            Student(
                name="James Dean",
                email="james.dean@gmail.com",
                phone="123-456-7890"
            ),
            Student(
                name="Jimmy Dean",
                email="jimmy.dean@gmail.com",
                phone="123-456-7890"
            ),
            Student(
                name="Howard Dean",
                email="howard.dean@gmail.com",
                phone="123-456-7890"
            ),
            Student(
                name="Brenda Dean",
                email="brenda.dean@gmail.com",
                phone="123-456-7890"
            ),
            Student(
                name="Felicity Dean",
                email="felicity.dean@gmail.com",
                phone="123-456-7890"
            )
        ]
        # Data for test cases.
        self.data = SimpleNamespace(
            add_student={
                "name": "John Cleese",
                "email": "john.cleese@gmail.com",
                "phone": "123-456-7890"
            },
            edit_student={
                "phone": "098-765-4321"
            },
            missing_key={
                "name": "John Cleese",
                "email": "john.cleese@gmail.com"
            },
            bad_key={
                "name": "John Cleese",
                "email": "john.cleese@gmail.com",
                "phone": "123-456-7890",
                "something_bad": "You don't want this in your data."
            },
            bad_phone={
                "name": "John Cleese",
                "email": "john.cleese@gmail.com",
                "phone": "123-456-789098765"
            },
            bad_email={
                "name": "John Cleese",
                "email": "john@cleese@gmail.com",
                "phone": "123-456-7890"
            },
            not_unique_email={
                "name": "James Dean",
                "email": "james.dean@gmail.com",
                "phone": "123-456-7890"
            },
            patch_not_unique_email={
                "name": "James R. Dean",
                "email": "james.dean@gmail.com"
            }
        )

    # Inserts seed data into database.
    def create_records(self):
        for course in self.seeds:
            course.insert()
