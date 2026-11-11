"""Students REST API built with Flask, the data is kept in memory."""

import copy
import os
from datetime import datetime, timezone

from flask import Flask, current_app, jsonify, request, url_for
from werkzeug.exceptions import HTTPException

API_PREFIX = "/api/v1.0"
STORE_KEY = "student_store"
DEFAULT_PORT = 5000
MAX_PORT = 65535
MIN_BIRTHYEAR = 1900
REQUIRED_FIELDS = ("name", "country", "city", "birthyear", "skills")

DEFAULT_STUDENTS = [
    {
        "name": "Anna",
        "country": "Finland",
        "city": "Helsinki",
        "birthyear": 1985,
        "skills": ["HTML", "CSS", "JavaScript", "Python"],
        "bio": "Loves automating boring tasks.",
    },
    {
        "name": "David",
        "country": "UK",
        "city": "London",
        "birthyear": 1990,
        "skills": ["Python", "MongoDB"],
        "bio": "Builds data pipelines.",
    },
    {
        "name": "John",
        "country": "Sweden",
        "city": "Stockholm",
        "birthyear": 1995,
        "skills": ["Java", "C#"],
        "bio": "Writes backend services.",
    },
]


class ValidationError(ValueError):
    """Student data sent by a client is not valid."""


class StudentNotFoundError(LookupError):
    """There is no student with the requested id."""


def _clean_text(field, value):
    """Return a stripped non-empty string.

    Args:
        field: Name of the field, used in the error message.
        value: Value to check.

    Returns:
        The value without spaces around it.

    Raises:
        ValidationError: If value is not a string or is blank.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"'{field}' must be a non-empty string")
    return value.strip()


def _clean_birthyear(field, value):
    """Return a birth year between MIN_BIRTHYEAR and the current year.

    Args:
        field: Name of the field, used in the error message.
        value: Value to check.

    Returns:
        The birth year.

    Raises:
        ValidationError: If value is not an int or is out of range.
    """
    current_year = datetime.now(timezone.utc).year
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(f"'{field}' must be an integer, got {value!r}")
    if not MIN_BIRTHYEAR <= value <= current_year:
        raise ValidationError(
            f"'{field}' must be between {MIN_BIRTHYEAR} and "
            f"{current_year}, got {value}"
        )
    return value


def _clean_skills(field, value):
    """Return stripped skills without case-insensitive duplicates.

    The first spelling and the order of the skills are kept.

    Args:
        field: Name of the field, used in the error message.
        value: Value to check.

    Returns:
        A new list of skills.

    Raises:
        ValidationError: If value is not a list of non-empty strings.
    """
    if not isinstance(value, list):
        raise ValidationError(f"'{field}' must be a list, got {value!r}")

    skills = {}
    for skill in value:
        cleaned = _clean_text(field, skill)
        skills.setdefault(cleaned.lower(), cleaned)
    return list(skills.values())


def _clean_bio(field, value):
    """Return a stripped string, an empty bio is allowed.

    Args:
        field: Name of the field, used in the error message.
        value: Value to check.

    Returns:
        The value without spaces around it.

    Raises:
        ValidationError: If value is not a string.
    """
    if not isinstance(value, str):
        raise ValidationError(f"'{field}' must be a string, got {value!r}")
    return value.strip()


CLEANERS = {
    "name": _clean_text,
    "country": _clean_text,
    "city": _clean_text,
    "birthyear": _clean_birthyear,
    "skills": _clean_skills,
    "bio": _clean_bio,
}


def validate_student(data, partial=False):
    """Check student data from a client and return a cleaned copy.

    Args:
        data: Student fields sent by the client.
        partial: If True, missing fields are allowed (PATCH) and bio
            gets no default.

    Returns:
        A new dict with the cleaned fields, the input is not changed.

    Raises:
        ValidationError: If data is not a dict, is empty, has unknown
            or missing fields, or a field has a wrong value.
    """
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")
    if not data:
        raise ValidationError("Request body must not be empty")

    unknown = sorted(set(data) - set(CLEANERS))
    if unknown:
        raise ValidationError(f"Unknown fields: {', '.join(unknown)}")

    if not partial:
        missing = [field for field in REQUIRED_FIELDS if field not in data]
        if missing:
            raise ValidationError(f"Missing fields: {', '.join(missing)}")

    cleaned = {
        field: CLEANERS[field](field, value) for field, value in data.items()
    }
    if not partial:
        cleaned.setdefault("bio", "")
    return cleaned


def _now():
    """Return the current UTC time in ISO format.

    Returns:
        A string like "2026-11-03T18:40:00+00:00".
    """
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class StudentStore:
    """Keep the students in memory and hand out copies of them."""

    def __init__(self, students=None):
        """Create a store and add the given students.

        Args:
            students: Valid student dicts to add, or None for an empty
                store.

        Raises:
            TypeError: If students is not a list or None.
        """
        if students is None:
            students = []
        if not isinstance(students, list):
            raise TypeError(f"students must be a list, got {students!r}")

        self._students = {}
        self._next_id = 1
        for student in students:
            self.add(student)

    def __len__(self):
        """Return the number of students.

        Returns:
            How many students are in the store.
        """
        return len(self._students)

    def _find(self, student_id):
        """Return the stored student itself, not a copy.

        Args:
            student_id: Id of the student.

        Returns:
            The student dict kept in the store.

        Raises:
            StudentNotFoundError: If there is no student with this id.
        """
        if student_id not in self._students:
            raise StudentNotFoundError(f"Student {student_id} not found")
        return self._students[student_id]

    def add(self, data):
        """Store a new student with the next id.

        Args:
            data: Valid student fields.

        Returns:
            A copy of the stored student with id, created_at and
            updated_at.
        """
        now = _now()
        student = {
            "id": self._next_id,
            **copy.deepcopy(data),
            "created_at": now,
            "updated_at": now,
        }
        self._students[self._next_id] = student
        self._next_id += 1
        return copy.deepcopy(student)

    def get(self, student_id):
        """Return one student.

        Args:
            student_id: Id of the student.

        Returns:
            A copy of the student.

        Raises:
            StudentNotFoundError: If there is no student with this id.
        """
        return copy.deepcopy(self._find(student_id))

    def list(self, country=None, skill=None):
        """Return the students sorted by id, optionally filtered.

        Both filters are case-insensitive exact matches.

        Args:
            country: Keep only students from this country.
            skill: Keep only students with this skill.

        Returns:
            A list of copies of the matching students.
        """
        students = sorted(
            self._students.values(), key=lambda student: student["id"]
        )
        if country:
            students = [
                student
                for student in students
                if student["country"].lower() == country.lower()
            ]
        if skill:
            wanted = skill.lower()
            students = [
                student
                for student in students
                if wanted in [known.lower() for known in student["skills"]]
            ]
        return copy.deepcopy(students)

    def update(self, student_id, data, partial=False):
        """Replace (PUT) or merge (PATCH) the data of a student.

        The id and created_at never change, updated_at is refreshed.

        Args:
            student_id: Id of the student.
            data: Valid student fields.
            partial: If True, merge data into the student instead of
                replacing it.

        Returns:
            A copy of the updated student.

        Raises:
            StudentNotFoundError: If there is no student with this id.
        """
        student = self._find(student_id)
        fields = copy.deepcopy(data)
        if partial:
            fields = {**student, **fields}

        self._students[student_id] = {
            **fields,
            "id": student_id,
            "created_at": student["created_at"],
            "updated_at": _now(),
        }
        return copy.deepcopy(self._students[student_id])

    def delete(self, student_id):
        """Remove a student, its id is never used again.

        Args:
            student_id: Id of the student.

        Raises:
            StudentNotFoundError: If there is no student with this id.
        """
        self._find(student_id)
        del self._students[student_id]


def _store():
    """Return the store of the current app.

    Returns:
        The StudentStore kept on the app by create_app().
    """
    return current_app.extensions[STORE_KEY]


def _query_filter(name):
    """Return a query string filter, None if it is missing or empty.

    Args:
        name: Name of the query parameter.

    Returns:
        The stripped value, or None for no filter.

    Raises:
        ValidationError: If the value has only spaces.
    """
    value = request.args.get(name, "")
    if value and not value.strip():
        raise ValidationError(f"'{name}' filter must not be blank")
    return value.strip() or None


def health():
    """Tell that the API is running.

    Returns:
        {"status": "ok"}.
    """
    return {"status": "ok"}


def list_students():
    """Return the students, filtered by ?country= and ?skill=.

    Returns:
        The list of students.

    Raises:
        ValidationError: If a filter has only spaces.
    """
    return jsonify(
        _store().list(
            country=_query_filter("country"), skill=_query_filter("skill")
        )
    )


def get_student(student_id):
    """Return one student.

    Args:
        student_id: Id from the URL.

    Returns:
        The student.

    Raises:
        StudentNotFoundError: If there is no student with this id.
    """
    return _store().get(student_id)


def create_student():
    """Create a student from the JSON body.

    Returns:
        The created student, status 201 and the Location header.

    Raises:
        ValidationError: If the body is not valid student data.
    """
    data = validate_student(request.get_json(silent=True))
    student = _store().add(data)
    location = url_for("get_student", student_id=student["id"])
    return student, 201, {"Location": location}


def replace_student(student_id):
    """Replace all the data of a student (PUT).

    Args:
        student_id: Id from the URL.

    Returns:
        The updated student.

    Raises:
        StudentNotFoundError: If there is no student with this id.
        ValidationError: If the body is not valid student data.
    """
    data = validate_student(request.get_json(silent=True))
    return _store().update(student_id, data)


def patch_student(student_id):
    """Change only the fields sent in the body (PATCH).

    Args:
        student_id: Id from the URL.

    Returns:
        The updated student.

    Raises:
        StudentNotFoundError: If there is no student with this id.
        ValidationError: If the body is empty or has a wrong value.
    """
    data = validate_student(request.get_json(silent=True), partial=True)
    return _store().update(student_id, data, partial=True)


def delete_student(student_id):
    """Delete a student.

    Args:
        student_id: Id from the URL.

    Returns:
        An empty body with status 204.

    Raises:
        StudentNotFoundError: If there is no student with this id.
    """
    _store().delete(student_id)
    return "", 204


def handle_validation_error(error):
    """Turn a ValidationError into a JSON 400 response.

    Args:
        error: The raised ValidationError.

    Returns:
        {"error": message} with status 400.
    """
    return {"error": str(error)}, 400


def handle_not_found(error):
    """Turn a StudentNotFoundError into a JSON 404 response.

    Args:
        error: The raised StudentNotFoundError.

    Returns:
        {"error": message} with status 404.
    """
    return {"error": str(error)}, 404


def handle_http_error(error):
    """Turn a Flask HTTP error (404, 405, ...) into JSON.

    The headers of the error, such as Allow for 405, are kept.

    Args:
        error: The raised HTTPException.

    Returns:
        The error response with {"error": description} as the body.
    """
    response = error.get_response()
    response.data = jsonify(error=error.description).get_data()
    response.content_type = "application/json"
    return response


def create_app(config=None):
    """Create a Flask app with its own student store.

    Args:
        config: Settings to apply on top of the defaults, e.g.
            {"SEED_DATA": []} to start with no students.

    Returns:
        The configured Flask app.

    Raises:
        TypeError: If config is not a dict or None.
    """
    if config is not None and not isinstance(config, dict):
        raise TypeError(f"config must be a dict, got {config!r}")

    app = Flask(__name__)
    app.config["SEED_DATA"] = DEFAULT_STUDENTS
    app.config.update(config or {})
    app.extensions[STORE_KEY] = StudentStore(app.config["SEED_DATA"])

    students_url = f"{API_PREFIX}/students"
    student_url = f"{students_url}/<int:student_id>"
    app.get(f"{API_PREFIX}/health")(health)
    app.get(students_url)(list_students)
    app.post(students_url)(create_student)
    app.get(student_url)(get_student)
    app.put(student_url)(replace_student)
    app.patch(student_url)(patch_student)
    app.delete(student_url)(delete_student)

    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(StudentNotFoundError, handle_not_found)
    app.register_error_handler(HTTPException, handle_http_error)
    return app


def read_port():
    """Read the server port from the PORT environment variable.

    Returns:
        The port, DEFAULT_PORT if PORT is not set.

    Raises:
        ValueError: If PORT is not a whole number between 1 and
            MAX_PORT.
    """
    value = os.environ.get("PORT", str(DEFAULT_PORT))
    try:
        port = int(value)
    except ValueError as error:
        raise ValueError(
            f"PORT must be a whole number, got {value!r}"
        ) from error
    if not 1 <= port <= MAX_PORT:
        raise ValueError(f"PORT must be between 1 and {MAX_PORT}, got {port}")
    return port


def main():
    """Run the development server on the port from PORT."""
    try:
        port = read_port()
    except ValueError as error:
        print(f"Cannot start the server: {error}")
        return

    create_app().run(port=port)


if __name__ == "__main__":
    main()
