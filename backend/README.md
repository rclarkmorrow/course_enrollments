# Course Enrollments API

Course enrollments is a minimal systems for creating courses, instructors and students and provides the ability to enroll students in courses, assign instructors to courses. Users can view course information, including course information with details about enrolled students or assigned instructors. Users can also view student and instructor information, including with detail about the courses a student or instructor is enrolled in or assigned to.

Anyone can view courses and course information, but other functions require authentication.

Authentication is provided by Auth0, and covers the following roles:

* Instructor: 
	* create and edit courses
* Registrar: 
	* can create, edit, and delete students. 
	* can view courses with enrolled students, and assigned instructors
	* can view courses a student is enrolled in
	* can view courses an instructor is assigned to
* Dean:
	* has all permissions for instructor and registrar role
	* can delete courses
	* can create, edit, and delete instructors.


This API can be cloned and run locally, but a live version is also hosted at heroku.


## Getting Started


### Obtaining Authorization Headers

Authorization headers can be obtained through [this link](https://rclarkmorrow.auth0.com/authorize?audience=course-enrollments-services&response_type=token&client_id=vsWulCF5Hcv5iFzlSQLxKuzSAcApam2c&redirect_uri=http://localhost:8100/) (see below) using the provided test user logins:
```
https://rclarkmorrow.auth0.com/authorize?audience=course-enrollments-services&response_type=token&client_id=vsWulCF5Hcv5iFzlSQLxKuzSAcApam2c&redirect_uri=http://localhost:8100/
```

You can also uncomment print statements in `/src/test_api.py` to print bearer tokens to the console.
#### Instructor
email: instructor@rclark.morrow.com<br />
password: TestInstructor1

#### Registrar
email: registrar@rclark.morrow.com<br />
password: TestRegistrar1

#### Dean
email: dean@rclark.morrow.com<br />
password: TestDean1

#### Test on Heroku

The API can be accessed at this [base URL](https://course-enrollments.herokuapp.com):

```
https://course-enrollments.herokuapp.com
```

## Run Local

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Configuration

The configurations settings for the app are included in the `/src/config/config.py` file. You can setup a `.env` file with environmental variables, or change the defaults in `config.py`.

Examples of settings you can configure:

* Page length for pagination
* Database and test database paths
* Auth0 settings
* Test users and passwords
* HTTP error messages

## Database Setup
Setup a database and test database with Postgresql.

With Postgresql running, and your database and test database paths configured you can run `src/drop_and_create_db.py` to initialize the database with seed data. 

_NOTE: this is meant for testing do not run this after database is on production because it will drop all of the tables, and revert to the seed data._

## Running the Server

From within the `src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=api.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

## Testing

###Postman tests
Postman collections are provided for both localhost, and heroku (some tests in the heroku collection may fail if the database has not been re-initialized after a prior run -- if that's the case you may want to record GET request data, and alter PATCH/DELETE requests to use existing uids).

With the seed data setup, you can update the included Postman collections with your authorization headers and verify that authorization is behaving as expected. You will likely want to re-initialize the database after running this test.
###Unittests
You should also be able to run `src/test_api.py` as soon as your test database and test database paths are configured. It should automatically obtain the necessary authorization tokens required for the tests.



## Endpoints

### Courses Information
Roles requried: none

Method: GET

URI: `/courses`

Request Arguments _(optional)_:

* detail=short, detail=full _(default)_
* page=<int>

Returns a list of courses with instructor names, or a list of courses with truncated details. Including a page argument returns paginated data.


```
GET '/courses'

Will return data in the following structure:

{
    "courses": [
        {
            "days": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday"
            ],
            "description": "This course is probably totally useless.",
            "end time": "09:00",
            "instructors": [
                {
                    "name": "Charles Francis Xavier",
                    "uid": 1
                },
                {
                    "name": "Ned Brainard",
                    "uid": 2
                }
            ],
            "start time": "07:30",
            "title": "Underwater Basket Weaving 101",
            "uid": 1
        },
        {
            "days": [
                "Tuesday",
                "Thursday"
            ],
            "description": "Advanced topics in useless skills.",
            "end time": "14:30",
            "instructors": [
                {
                    "name": "Ned Brainard",
                    "uid": 2
                }
            ],
            "start time": "12:00",
            "title": "Underwater Basket Weaving 201",
            "uid": 2
        },
        {
            "days": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday"
            ],
            "description": "Stuff is happening on the internet.",
            "end time": "10:00",
            "instructors": [
                {
                    "name": "Professor Plum",
                    "uid": 3
                }
            ],
            "start time": "08:30",
            "title": "New Trends in Digital Life",
            "uid": 3
        },
        {
            "days": [
                "Monday",
                "Wednesday",
                "Friday"
            ],
            "description": "Have considered bears lately? Think about them in new ways.",
            "end time": "13:00",
            "instructors": [
                {
                    "name": "John Keating",
                    "uid": 4
                }
            ],
            "start time": "10:30",
            "title": "Bears - A New Biological Framework",
            "uid": 4
        },
        {
            "days": [
                "Monday",
                "Friday"
            ],
            "description": "They do. We'll explain.",
            "end time": "16:00",
            "instructors": [
                {
                    "name": "The Doctor",
                    "uid": 5
                }
            ],
            "start time": "14:30",
            "title": "Why People Love Music",
            "uid": 5
        }
    ],
    "success": true,
    "total_records": 5
}

GET '/courses?detail=short

{
    "courses": [
        {
            "title": "Underwater Basket Weaving 101",
            "uid": 1
        },
        {
            "title": "Underwater Basket Weaving 201",
            "uid": 2
        },
        {
            "title": "New Trends in Digital Life",
            "uid": 3
        },
        {
            "title": "Bears - A New Biological Framework",
            "uid": 4
        },
        {
            "title": "Why People Love Music",
            "uid": 5
        }
    ],
    "success": true,
    "total_records": 5
}
```

### Course Information
Roles requried: none

Method: GET

URI: `/courses/<uid>`

Request Arguments: None

Returns full details on a single course.

```

GET '/courses/1'

Will return data in the following structure:

{
    "course": {
        "days": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ],
        "description": "This course is probably totally useless.",
        "end time": "09:00",
        "instructors": [
            {
                "name": "Charles Francis Xavier",
                "uid": 1
            },
            {
                "name": "Ned Brainard",
                "uid": 2
            }
        ],
        "start time": "07:30",
        "title": "Underwater Basket Weaving 101",
        "uid": 1
    },
    "success": true
}

```

### Course Details with Students
Roles required: Registrar or Dean

Method: GET

Request Arguments: None

URI: `/courses/<uid>/students`

Returns full details on a single course, with full details of enrolled students.


```
GET '/courses/1/students'

Will return data in the following structure:

{
    "course": {
        "days": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ],
        "description": "This course is probably totally useless.",
        "end time": "09:00",
        "start time": "07:30",
        "students": [
            {
                "email": "james.dean@gmail.com",
                "enrollment_uid": 1,
                "name": "James Dean",
                "phone": "123-456-7890",
                "uid": 1
            },
            {
                "email": "jimmy.dean@gmail.com",
                "enrollment_uid": 6,
                "name": "Jimmy Dean",
                "phone": "123-456-7890",
                "uid": 2
            }
        ],
        "title": "Underwater Basket Weaving 101",
        "uid": 1
    },
    "success": true
}
```

### Course Details with Instructors
Roles required: Registrar or Dean

Method: GET

Request Arguments: None
 
URI: `courses/uid>/instructors`

Returns full details on a single course, with full details of assigned instructors.


```
GET '/courses/1/instructors'

Will return data in the following structure:

{
    "course": {
        "days": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ],
        "description": "This course is probably totally useless.",
        "end time": "09:00",
        "instructors": [
            {
                "assignment_uid": 1,
                "email": "charles.f.xavier@university.edu",
                "name": "Charles Francis Xavier",
                "phone": "123-456-7890",
                "uid": 1
            },
            {
                "assignment_uid": 6,
                "email": "ned.brainard@university.edu",
                "name": "Ned Brainard",
                "phone": "123-456-7890",
                "uid": 2
            }
        ],
        "start time": "07:30",
        "title": "Underwater Basket Weaving 101",
        "uid": 1
    },
    "success": true
}
```

### Creating a Course
Roles required: Instructor or Dean

Method: POST

URI: `/courses`

Must include all keys(see JSON Request Body below).

Adds a new course to the database.

```
POST '/courses'
JSON Request Body:

{
    "title": "The Science of Science",
    "days": [
        "Monday",
        "Wednesday",
        "Friday"
    ],
    "start_time": "10:30",
    "end_time": "12:00",
    "description": "There's a science to it."
}

Returns:

{
    "message": "course created",
    "success": true
}
```

### Editing a Course
Roles required: Instructor or Dean

Method: PATCH

URI: `/courses/<uid>`

Can include any combination of avaiable keys (see JSON Request Body for example).

Edits a course in the database.

```
PATCH '/courses/1'

JSON Request Body:

{
    "description": "Let's change a course description!"
}

Returns:

{
    "message": "updated course with uid: 1",
    "success": true
}
```

### Deleting a Course
Roles required: Dean

Method: DELETE

URI: `/courses/<uid>`

Delets a course from the database.

```
DELETE '/courses/1'

Returns:

{
    "message": "deleted course with uid: 1",
    "success": true
}
```

### Students Information
Roles requried: Registrar or Dean

Method: GET

URI: `/students`

Request Arguments _(optional)_:

* detail=short, detail=full _(default)_
* page=<int>

Returns a list of students, or a list of students with truncated details. Including a page argument returns paginated data.


```
GET '/students'

Will return data in the following structure:

{
    "students": [
        {
            "email": "james.dean@gmail.com",
            "name": "James Dean",
            "phone": "123-456-7890",
            "uid": 1
        },
        {
            "email": "jimmy.dean@gmail.com",
            "name": "Jimmy Dean",
            "phone": "123-456-7890",
            "uid": 2
        },
        {
            "email": "howard.dean@gmail.com",
            "name": "Howard Dean",
            "phone": "123-456-7890",
            "uid": 3
        },
        {
            "email": "brenda.dean@gmail.com",
            "name": "Brenda Dean",
            "phone": "123-456-7890",
            "uid": 4
        },
        {
            "email": "felicity.dean@gmail.com",
            "name": "Felicity Dean",
            "phone": "123-456-7890",
            "uid": 5
        }
    ],
    "success": true,
    "total_records": 5
}

GET '/students?detail=short

{
    "students": [
        {
            "name": "James Dean",
            "uid": 1
        },
        {
            "name": "Jimmy Dean",
            "uid": 2
        },
        {
            "name": "Howard Dean",
            "uid": 3
        },
        {
            "name": "Brenda Dean",
            "uid": 4
        },
        {
            "name": "Felicity Dean",
            "uid": 5
        }
    ],
    "success": true,
    "total_records": 5
}
```

### Student Information
Roles requried: Registrar or Dean

Method: GET

URI: `/students/<uid>`

Request Arguments: None

Returns full details on a single student.

```

GET '/students/1'

Will return data in the following structure:

{
    "student": {
        "email": "james.dean@gmail.com",
        "name": "James Dean",
        "phone": "123-456-7890",
        "uid": 1
    },
    "success": true
}

```

### Student Details with Courses
Roles required: Registrar or Dean

Method: GET

Request Arguments: None

URI: `/students/<uid>/courses`

Returns full details on a single student, with details of courses student is enrolled in.


```
GET '/students/2/courses'

Will return data in the following structure:

{
    "student": {
        "email": "jimmy.dean@gmail.com",
        "enrollments": [
            {
                "days": "tuesday,thursday",
                "end_time": "14:30",
                "start_time": "12:00",
                "title": "Underwater Basket Weaving 201",
                "uid": 2
            },
            {
                "days": "Monday,Tuesday,Wednesday,Thursday,Friday",
                "end_time": "09:00",
                "start_time": "07:30",
                "title": "Underwater Basket Weaving 101",
                "uid": 6
            }
        ],
        "name": "Jimmy Dean",
        "phone": "123-456-7890",
        "uid": 2
    },
    "success": true
}
```

### Creating a Student
Roles required: Registrar or Dean

Method: POST

URI: `/students`

Must include all keys(see JSON Request Body below).

Adds a new student to the database.

```
POST '/students'
JSON Request Body:

{
    "name": "John Cleese",
    "email": "john.cleese@gmail.com",
    "phone": "123-456-7890"
}

Returns:

{
    "message": "student created",
    "success": true
}
```

### Editing a Student
Roles required: Registrar or Dean

Method: PATCH

URI: `/students/<uid>`

Can include any combination of avaiable keys (see JSON Request Body for example).

Edits a student in the database.

```
PATCH '/students/1'

JSON Request Body:

{
    "name": "Let's change a name!"
}

Returns:

{
    "message": "updated student with uid: 1",
    "success": true
}
```

### Deleting a Student
Roles required: Registrar or Dean

Method: DELETE

URI: `/students/<uid>`

Deletes a student from the database.

```
DELETE '/students/1'

Returns:

{
    "message": "deleted student with uid: 1",
    "success": true
}
```

### Instructors Information
Roles requried: Registrar or Dean

Method: GET

URI: `/instructors`

Request Arguments _(optional)_:

* detail=short, detail=full _(default)_
* page=<int>

Returns a list of instructors, or a list of instructors with truncated details. Including a page argument returns paginated data.


```
GET '/instructors'

Will return data in the following structure:

{
    "instructors": [
        {
            "bio": "Attended the University of Oxford, where he earned a Professorship in Genetics and other science field",
            "email": "charles.f.xavier@university.edu",
            "name": "Charles Francis Xavier",
            "phone": "123-456-7890",
            "uid": 1
        },
        {
            "bio": "The famous inventor of flubber.",
            "email": "ned.brainard@university.edu",
            "name": "Ned Brainard",
            "phone": "123-456-7890",
            "uid": 2
        },
        {
            "bio": "A brilliant, if not controversial, psychiatrist",
            "email": "professor.plum@university.edu",
            "name": "Professor Plum",
            "phone": "123-456-7890",
            "uid": 3
        },
        {
            "bio": "O Captain?",
            "email": "john.keating@university.edu",
            "name": "John Keating",
            "phone": "123-456-7890",
            "uid": 4
        },
        {
            "bio": "Time keeps on ticking, ticking.",
            "email": "the.doctor@univserity.edu",
            "name": "The Doctor",
            "phone": "123-456-7890",
            "uid": 5
        }
    ],
    "success": true,
    "total_records": 5
}

GET '/instructors?detail=short

{
    "instructors": [
        {
            "bio": "Attended the University of Oxford, where he earned a Professorship in Genetics and other science field",
            "name": "Charles Francis Xavier",
            "uid": 1
        },
        {
            "bio": "The famous inventor of flubber.",
            "name": "Ned Brainard",
            "uid": 2
        },
        {
            "bio": "A brilliant, if not controversial, psychiatrist",
            "name": "Professor Plum",
            "uid": 3
        },
        {
            "bio": "O Captain?",
            "name": "John Keating",
            "uid": 4
        },
        {
            "bio": "Time keeps on ticking, ticking.",
            "name": "The Doctor",
            "uid": 5
        }
    ],
    "success": true,
    "total_records": 5
}
```

### Instructor Information
Roles requried: Registrar or Dean

Method: GET

URI: `/instructors/<uid>`

Request Arguments: None

Returns full details on a single instructor.

```

GET '/instructors/1'

Will return data in the following structure:

{
    "instructor": {
        "bio": "Attended the University of Oxford, where he earned a Professorship in Genetics and other science field",
        "email": "charles.f.xavier@university.edu",
        "name": "Charles Francis Xavier",
        "phone": "123-456-7890",
        "uid": 1
    },
    "success": true
}

```

### Instructor Details with Courses
Roles required: Registrar or Dean

Method: GET

Request Arguments: None

URI: `/instructors/<uid>/courses`

Returns full details on a single instructor, with details of courses instructor is assigned to.


```
GET '/instructors/2/courses'

Will return data in the following structure:

{
    "instructor": {
        "assignments": [
            {
                "days": "tuesday,thursday",
                "end_time": "14:30",
                "start_time": "12:00",
                "title": "Underwater Basket Weaving 201",
                "uid": 2
            },
            {
                "days": "Monday,Tuesday,Wednesday,Thursday,Friday",
                "end_time": "09:00",
                "start_time": "07:30",
                "title": "Underwater Basket Weaving 101",
                "uid": 6
            }
        ],
        "bio": "The famous inventor of flubber.",
        "email": "ned.brainard@university.edu",
        "name": "Ned Brainard",
        "phone": "123-456-7890",
        "uid": 2
    },
    "success": true
}
```

### Creating an Instructor
Roles required: Dean

Method: POST

URI: `/instructors`

Must include all keys(see JSON Request Body below).

Adds a new instructor to the database.

```
POST 'instructors/'
JSON Request Body:

{
    "name": "Dr. Strangelove",
    "email": "dr.strangelove@university.edu",
    "phone": "123-456-7890",
    "bio": "Specialized in teaching people how to stop worrying."
}

Returns:

{
    "message": "instructor created",
    "success": true
}
```

### Editing an Instructor
Roles required: Dean

Method: PATCH

URI: `/instructors/<uid>`

Can include any combination of avaiable keys (see JSON Request Body for example).

Edits an instructor in the database.

```
PATCH '/instructors/1'

JSON Request Body:

{
    "name": "Let's change a name!"
}

Returns:

{
    "message": "updated instructor with uid: 1",
    "success": true
}
```

### Deleting an Instructor
Roles required: Dean

Method: DELETE

URI: `/instructors/<uid>`

Deletes an instructor from the database.

```
DELETE '/instructors/1'

Returns:

{
    "message": "deleted instructor with uid: 1",
    "success": true
}
```

### Creating an Enrollment
Roles required: Registrar or Dean

Method: POST

URI: `/enrollments`

Must include all keys(see JSON Request Body below).

Adds a new enrollment to the database.

```
POST '/enrollments'
JSON Request Body:

{
    "course_uid": 1,
    "student_uid": 5

}

Returns:

{
    "message": "enrollment created",
    "success": true
}
```

### Deleting an Enrollment
Roles required: Registrar or Dean

Method: DELETE

URI: `/enrollments/<uid>`

Deletes an enrollment from the database.

```
DELETE '/enrolllments/1'

Returns:

{
    "message": "deleted enrollment with uid: 1",
    "success": true
}
```

### Creating an Assignment
Roles required: Dean

Method: POST

URI: `/assignments`

Must include all keys(see JSON Request Body below).

Adds a new assignment to the database.

```
POST '/assignments'
JSON Request Body:

{
    "course_uid": 1,
    "instructor_uid": 5

}

Returns:

{
    "message": "assignment created",
    "success": true
}
```

### Deleting an Assignment
Roles required: Dean

Method: DELETE

URI: `/assignments/<uid>`

Deletes an assignment from the database.

```
DELETE '/assignments/1'

Returns:

{
    "message": "deleted assignment with uid: 1",
    "success": true
}
```