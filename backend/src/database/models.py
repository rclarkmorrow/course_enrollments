""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


# Local applicaiton dependencies
from config.config import db


""" --------------------------------------------------------------------------#
# MODELS
# --------------------------------------------------------------------------"""


# Base Model: constains common methods.
# -----------------------------------------------------------------------------
class BaseModel:
    # Insert record.
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Update record.
    def update(self):
        db.session.commit()

    # Delete record.
    def delete(self):
        db.session.delete(self)
        db.session.commit()


# Student Model: Contains data about a student.
# -----------------------------------------------------------------------------
class Student(BaseModel, db.Model):
    # Main model
    __tablename__ = 'student'
    # Autoincrementing, unique primary key
    uid = db.Column(db.Integer(), primary_key=True)
    # Student data
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(120), nullable=False)
    # Relationships
    enrollments = db.relationship('Enrollment', back_populates='student',
                                  cascade='all,delete,delete-orphan')
    grades = db.relationship('Grade', back_populates='student',
                             cascade='all,delete,delete-orphan')

    # Methods
    def __init__(self, name=None, email=None, phone=None):
        self.name = name
        self.email = email
        self.phone = phone

    # Return full details.
    def full(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
        }

    # Return truncated details.
    def short(self):
        return {
            'uid': self.uid,
            'name': self.name
        }

    # Return full details with enrollments.
    def with_enrollments(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'enrollments': [{
                'uid': enrollment.uid,
                'title': enrollment.course.title,
                'days': enrollment.course.days,
                'start_time': enrollment.course.start_time,
                'end_time': enrollment.course.end_time
            } for enrollment in self.enrollments]
        }


# Instructor Model: Contains data about an instructor.
# -----------------------------------------------------------------------------
class Instructor(BaseModel, db.Model):
    # Main model
    __tablename__ = 'instructor'

    # Autoincrementing, unique primary key
    uid = db.Column(db.Integer(), primary_key=True)

    # Instructor data
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(129), nullable=False)
    bio = db.Column(db.String(1000), nullable=False)

    # Relationships
    assignments = db.relationship('Assignment', back_populates='instructor',
                                  cascade='all,delete,delete-orphan')
    grades = db.relationship('Grade', back_populates='instructor',
                             cascade='all,delete,delete-orphan')

    # Methods
    def __init__(self, name=None, email=None, phone=None, bio=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.bio = bio

# Return full details.
    def full(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'bio': self.bio
        }

    # Return truncated details.
    def short(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'bio': self.bio
        }

    # Return full details with assignments.
    def with_assignments(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'bio': self.bio,
            'assignments': [{
                'uid': assignment.uid,
                'title': assignment.course.title,
                'days': assignment.course.days,
                'start_time': assignment.course.start_time,
                'end_time': assignment.course.end_time
            } for assignment in self.assignments]
        }


# Course Model -- Contains data about a course.
# ------------------------------------------------------------------------
class Course(BaseModel, db.Model):
    __tablename__ = 'course'

    # Autoincrementing, unique primary key
    uid = db.Column(db.Integer(), primary_key=True)

    # Course data
    title = db.Column(db.String(120), nullable=False)
    days = db.Column(db.String(240), nullable=False)
    start_time = db.Column(db.String(120), nullable=False)
    end_time = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    # Relationships
    assignments = db.relationship('Assignment', back_populates='course',
                                  cascade='all,delete,delete-orphan')
    enrollments = db.relationship('Enrollment', back_populates='course',
                                  cascade='all,delete,delete-orphan')
    # enrollments = db.relationship('Enrollment', back_populates='student',
    #                               lazy=True)

    # Methods
    def __init__(self, title=None, days=None,
                 start_time=None, end_time=None, description=None):
        self.title = title
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.description = description

    # Return full details
    def full(self):
        return {
            'uid': self.uid,
            'title': self.title,
            'instructors': [{
                'uid': assignment.instructor.uid,
                'name': assignment.instructor.name,
            } for assignment in self.assignments],
            'days': (
                [day.capitalize() for day in self.days.split(',')]
                if type(self.days) != list else self.days
                ),
            'start time': self.start_time,
            'end time': self.end_time,
            'description': self.description
        }

    # Return truncated details.
    def short(self):
        return {
            'uid': self.uid,
            'title': self.title
        }

    def with_students(self):
        return {
            'uid': self.uid,
            'title': self.title,
            'students': [{
                'uid': enrollment.student.uid,
                'name': enrollment.student.name,
                'email': enrollment.student.email,
                'phone': enrollment.student.phone,
                'enrollment_uid': enrollment.uid
            } for enrollment in self.enrollments],
            'days': (
                [day.capitalize() for day in self.days.split(',')]
                if type(self.days) != list else self.days
                ),
            'start time': self.start_time,
            'end time': self.end_time,
            'description': self.description
        }

    def with_instructors(self):
        return {
            'uid': self.uid,
            'title': self.title,
            'instructors': [{
                'uid': assignment.instructor.uid,
                'name': assignment.instructor.name,
                'email': assignment.instructor.email,
                'phone': assignment.instructor.phone,
                'assignment_uid': assignment.uid
            } for assignment in self.assignments],
            'days': (
                [day.capitalize() for day in self.days.split(',')]
                if type(self.days) != list else self.days
                ),
            'start time': self.start_time,
            'end time': self.end_time,
            'description': self.description
        }


# Assignment Model: Registers instructor to teach a course.
# ------------------------------------------------------------------------
class Assignment (BaseModel, db.Model):
    # Main model
    __tablename__ = 'assignment'
    # Autoincrementing, unique primary key
    uid = db.Column(db.Integer, primary_key=True)
    # Assignment data
    course_uid = db.Column(db.Integer, db.ForeignKey('course.uid',),
                           nullable=False)
    instructor_uid = db.Column(db.Integer, db.ForeignKey('instructor.uid'),
                               nullable=False)

    # Relationship
    course = db.relationship('Course', back_populates='assignments', lazy=True)
    instructor = db.relationship('Instructor', back_populates='assignments',
                                 lazy=True)


# Enrollment model - Registers a student for a course.
# ------------------------------------------------------------------------
class Enrollment(BaseModel, db.Model):
    # Main model
    __tablename__ = 'enrollment'
    # Autoincrementing, unique primary key
    uid = db.Column(db.Integer, primary_key=True)
    # Enrollment data
    course_uid = db.Column(db.Integer, db.ForeignKey('course.uid'),
                           nullable=False)
    student_uid = db.Column(db.Integer, db.ForeignKey('student.uid'),
                            nullable=False)

    # Relationships
    course = db.relationship('Course', back_populates='enrollments', lazy=True)
    student = db.relationship('Student', back_populates='enrollments',
                              lazy=True)


# Enrollment model - Registers a student for a course.
# ------------------------------------------------------------------------
class Grade(BaseModel, db.Model):
    # Main model
    __tablename__ = 'grade'
    # Autoincrementing, unique primary key
    uid = db.Column(db.Integer, primary_key=True)
    # Grade data
    student_uid = db.Column(db.Integer, db.ForeignKey('student.uid'),
                            nullable=False)
    course_uid = db.Column(db.Integer, db.ForeignKey('course.uid'),
                           nullable=False)
    grade = db.Column(db.String(120), nullable=False)
