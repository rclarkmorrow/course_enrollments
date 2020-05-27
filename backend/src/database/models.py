""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


# Third party dependencies
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

# Local applicaiton dependencies
from config.config import db



""" --------------------------------------------------------------------------#
# MODELS
# --------------------------------------------------------------------------"""


# Student Model: Contains data about a student.
# -----------------------------------------------------------------------------
class Student(db.Model):
    # Main model
    __tablename__ = 'student'
    # Autoincrementing, unique primary key
    uid = db.Column(db.Integer(), primary_key=True)
    # Student data
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(120), nullable=False)
    # Relationships
    enrollments = db.relationship('Enrollment', back_populates='student')

    # Methods
    def __init__(self, name=None, email=None, phone=None):
        self.name = name
        self.email = email
        self.phone = phone

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
class Instructor(db.Model):
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
    assignments = db.relationship('Assignment', back_populates='instructor')

    # Methods
    def __init__(self, name=None, email=None, phone=None, bio=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.bio = bio

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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

    # Return full details with enrollments.
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
class Course(db.Model):
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
    assignments = db.relationship('Assignment', back_populates='course')
    enrollments = db.relationship('Enrollment', back_populates='course')
    # enrollments = db.relationship('Enrollment', back_populates='student',
    #                               lazy=True)

    # Methods
    def __init__(self, title=None, days=None, hour=None,
                 start_time=None, end_time=None, description=None):
        self.title = title
        self.days = days
        self.hour = hour
        self.start_time = start_time
        self.end_time = end_time
        self.description = description

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


# Assignment Model: Registers instructor to teach a course.
# ------------------------------------------------------------------------
class Assignment (db.Model):
    # Main model
    __tablename__ = 'assignment'
    # Autoincrementing, unique primary key
    uid = db.Column(db.Integer, primary_key=True)
    # Assignment data
    course_uid = db.Column(db.Integer, db.ForeignKey('course.uid',
                           ondelete='CASCADE'), nullable=False)
    instructor_uid = db.Column(db.Integer, db.ForeignKey('instructor.uid'),
                               nullable=False)

    # Relationship
    course = db.relationship('Course', back_populates='assignments', lazy=True)
    instructor = db.relationship('Instructor', back_populates='assignments',
                                 lazy=True)

    # Methods
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# Enrollment model - Registers a student for a course.
# ------------------------------------------------------------------------
class Enrollment(db.Model):
    # Main model
    __tablename__ = 'enrollment'
    # Autoincrementing, unique primary key
    uid = db.Column(db.Integer, primary_key=True)
    # Enrollment data
    course_uid = db.Column(db.Integer, db.ForeignKey('course.uid',
                           ondelete='CASCADE'), nullable=False)
    student_uid = db.Column(db.Integer, db.ForeignKey('student.uid'),
                            nullable=False)

    # Relationships
    course = db.relationship('Course', back_populates='enrollments', lazy=True)
    student = db.relationship('Student', back_populates='enrollments',
                              lazy=True)

    # Methods
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
