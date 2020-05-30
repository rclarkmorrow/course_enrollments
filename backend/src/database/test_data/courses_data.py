""" ---------------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------------"""


# Standard library dependencies
from types import SimpleNamespace

# Local application dependencies
from database.models import Course


""" ---------------------------------------------------------------------------
# TEST DATA CLASS
# --------------------------------------------------------------------------"""


# Class initializes with test data, and methods to populate test database.
# -----------------------------------------------------------------------------
class CourseTest:
    def __init__(self):
        # Seed data for test database
        self.seeds = [
            Course(
                title="Underwater Basket Weaving 101",
                days="Monday,Tuesday,Wednesday,Thursday,Friday",
                start_time="07:30",
                end_time="09:00",
                description="This course is probably totally useless."
            ),
            Course(
                title="Underwater Basket Weaving 201",
                days="tuesday,thursday",
                start_time="12:00",
                end_time="14:30",
                description="Advanced topics in useless skills."
            ),
            Course(
                title="New Trends in Digital Life",
                days="Monday,Tuesday,Wednesday,Thursday,Friday",
                start_time="08:30",
                end_time="10:00",
                description="Stuff is happening on the internet."
            ),
            Course(
                title="Bears - A New Biological Framework",
                days="Monday,Wednesday,Friday",
                start_time="10:30",
                end_time="13:00",
                description=("Have considered bears lately? Think about them" 
                             " in new ways.")
            ),
            Course(
                title="Why People Love Music",
                days="Monday,Friday",
                start_time="14:30",
                end_time="16:00",
                description="They do. We'll explain."
            )
        ]
        # Data for test cases.
        self.data = SimpleNamespace(
            add_course={
                "title": "The Science of Science",
                "days": [
                    "Monday",
                    "Wednesday",
                    "Friday"
                ],
                "start_time": "10:30",
                "end_time": "12:00",
                "description": "There's a science to it."
            },
            edit_course={
                "description": "Let's change a course description!"
            },
            edit_course_time={
                "start_time": "08:00"
            },
            missing_key={
                "title": "The Science of Science",
                "start_time": "14:30",
                "end_time": "16:00",
                "description": "There's a science to it."
            },
            bad_key={
                "title": "The Science of Science",
                "days": [
                    "Monday",
                    "Wednesday",
                    "Friday",
                ],
                "start_time": "14:30",
                "end_time": "16:00",
                "description": "There's a science to it.",
                "something_bad": "You don't want this in your data."
            },
            duplicate_day={
                "title": "The Science of Science",
                "days": [
                    "Wednesday",
                    "Monday",
                    "Friday",
                    "Wednesday"
                ],
                "start_time": "14:30",
                "end_time": "16:00",
                "description": "There's a science to it."
            },
            day_not_list={
                "title": "The Science of Science",
                "days": "Monday, Friday",
                "start_time": "14:30",
                "end_time": "16:00",
                "description": "There's a science to it."
            },
            bad_day={
                "title": "The Science of Science",
                "days": [
                    "Good Friday",
                    "Monday",
                    "Friday",
                ],
                "start_time": "12:00",
                "end_time": "01:30",
                "description": "There's a science to it."
            },
            start_early={
                "title": "The Science of Science",
                "days": [
                    "Monday",
                    "Wednesday",
                    "Friday",
                ],
                "start_time": "07:00",
                "end_time": "08:30",
                "description": "There's a science to it."
            },
            start_late={
                "title": "The Science of Science",
                "days": [
                    "Monday",
                    "Wednesday",
                    "Friday",
                ],
                "start_time": "18:30",
                "end_time": "20:00",
                "description": "There's a science to it."
            },
            start_after_end={
                "title": "The Science of Science",
                "days": [
                    "Monday",
                    "Wednesday",
                    "Friday",
                ],
                "start_time": "12:30",
                "end_time": "10:30",
                "description": "There's a science to it."
            },
            bad_time={
                "title": "The Science of Science",
                "days": [
                    "Monday",
                    "Wednesday",
                    "Friday",
                ],
                "start_time": "12:30:45",
                "end_time": "13:30",
                "description": "There's a science to it."
            },
            conflict_time={
                "start_time": "12:30",
                "end_time": "13:00"
            }
        )

    # Inserts seed data into database.
    def create_records(self):
        for course in self.seeds:
            course.insert()
