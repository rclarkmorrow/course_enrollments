""" ---------------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------------"""


# Standard library dependencies
from types import SimpleNamespace

# Local application dependencies
from database.models import Instructor


""" ---------------------------------------------------------------------------
# TEST DATA CLASS
# --------------------------------------------------------------------------"""


# Class initializes with test data, and methods to populate test database.
# -----------------------------------------------------------------------------
class InstructorTest:
    def __init__(self):
        # Seed data for test database
        self.seeds = [
            Instructor(
                name="Charles Francis Xavier",
                email="charles.f.xavier@university.edu",
                phone="123-456-7890",
                bio=("Attended the University of Oxford, where he earned a"
                     " Professorship in Genetics and other science field")
            ),
            Instructor(
                name="Ned Brainard",
                email="ned.brainard@university.edu",
                phone="123-456-7890",
                bio="The famous inventor of flubber."
            ),
            Instructor(
                name="Professor Plum",
                email="professor.plum@university.edu",
                phone="123-456-7890",
                bio="A brilliant, if not controversial, psychiatrist"
            ),
            Instructor(
                name="John Keating",
                email="john.keating@university.edu",
                phone="123-456-7890",
                bio="O Captain?"
            ),
            Instructor(
                name="The Doctor",
                email="the.doctor@univserity.edu",
                phone="123-456-7890",
                bio="Time keeps on ticking, ticking."
            )
        ]
        # Data for test cases.
        self.data = SimpleNamespace(
            add_instructor={
                "name": "Dr. Strangelove",
                "email": "dr.strangelove@university.edu",
                "phone": "123-456-7890",
                "bio": "Specialized in teaching people how to stop worrying."
            },
            edit_instructor={
                "phone": "098-765-4321"
            },
            missing_key={
                "name": "Dr. Strangelove",
                "email": "dr.strangelove@university.edu"
            },
            bad_key={
                "name": "Dr. Strangelove",
                "email": "dr.strangelove@university.edu",
                "phone": "123-456-7890",
                "bio": "Specialized in teaching people how to stop worrying.",
                "something_bad": "You don't want this in your data."
            },
            bad_phone={
                "name": "Dr. Strangelove",
                "email": "dr.strangelove@university.edu",
                "phone": "123-456-789098765",
                "bio": "Specialized in teaching people how to stop worrying."

            },
            bad_email={
                "name": "Dr. Strangelove",
                "email": "dr@strangelove@university.edu",
                "phone": "123-456-7890",
                "bio": "Specialized in teaching people how to stop worrying.",
            },
            not_unique_email={
                "name": "Charles Francis Xavier",
                "email": "charles.f.xavier@university.edu",
                "phone": "123-456-7890",
                "bio": ("Attended the University of Oxford, where he earned a"
                        " Professorship in Genetics and other science field")
            },
            patch_not_unique_email={
                "name": "Charles Xavier",
                "email": "charles.f.xavier@university.edu"
            }
        )

    # Inserts seed data into database.
    def create_records(self):
        for course in self.seeds:
            course.insert()
