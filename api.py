import re
from flask import Blueprint, request, jsonify, url_for, current_app
from sqlalchemy.exc import IntegrityError
from models import db, Student

api_bp = Blueprint("api", __name__)

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def json_error(message, status=400, details=None):
    payload = {"error": True, "message": message}
    if details is not None:
        payload["details"] = details
    return jsonify(payload), status


def validate_student_payload(data, partial=False):
    errors = []
    cleaned = {}

    if not isinstance(data, dict):
        return {}, ["JSON body must be an object"]

    # student_id
    if "student_id" in data:
        if not data["student_id"] or not str(data["student_id"]).strip():
            errors.append("student_id cannot be empty")
        else:
            cleaned["student_id"] = str(data["student_id"]).strip()
    elif not partial:
        errors.append("student_id is required")

    # name
    if "name" in data:
        if not data["name"] or not str(data["name"]).strip():
            errors.append("name cannot be empty")
        else:
            cleaned["name"] = str(data["name"]).strip()
    elif not partial:
        errors.append("name is required")

    # email
    if "email" in data:
        email = str(data["email"]).strip()
        if not EMAIL_RE.match(email):
            errors.append("email is not a valid email address")
        else:
            cleaned["email"] = email
    elif not partial:
        errors.append("email is required")

    # age
    if "age" in data:
        try:
            age_val = int(data["age"]) if data["age"] is not None and data["age"] != "" else None
            if age_val is not None and age_val < 0:
                errors.append("age must be >= 0")
            else:
                cleaned["age"] = age_val
        except (TypeError, ValueError):
            errors.append("age must be an integer")

    # marks
    if "marks" in data:
        marks = data["marks"]
        if marks is None:
            cleaned["marks"] = []
        elif not isinstance(marks, (list, tuple)):
            errors.append("marks must be a list of numbers")
        else:
            normalized = []
            for i, v in enumerate(marks):
                try:
                    normalized.append(float(v))
                except (TypeError, ValueError):
                    errors.append(f"marks[{i}] is not numeric")
            if not errors:
                cleaned["marks"] = normalized

    return cleaned, errors


@api_bp.route("/students", methods=["GET"])
def list_students():
    students = Student.query.order_by(Student.id.asc()).all()
    return jsonify([s.to_dict() for s in students]), 200


@api_bp.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    s = Student.query.get(student_id)
    if not s:
        return json_error("Student not found", status=404)
    return jsonify(s.to_dict()), 200


@api_bp.route("/students", methods=["POST"])
def create_student():
    data = request.get_json(silent=True)
    if data is None:
        return json_error("Invalid or missing JSON body", status=400)

    cleaned, errors = validate_student_payload(data, partial=False)
    if errors:
        return json_error("Validation failed", status=400, details=errors)

    if Student.query.filter_by(student_id=cleaned["student_id"]).first():
        return json_error("student_id already exists", status=409)
    if Student.query.filter_by(email=cleaned["email"]).first():
        return json_error("email already exists", status=409)

    try:
        s = Student.from_dict(cleaned)
        db.session.add(s)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        current_app.logger.exception("Integrity error creating student")
        return json_error("Database integrity error", status=409)
    except Exception:
        db.session.rollback()
        current_app.logger.exception("Error creating student")
        return json_error("Internal server error", status=500)

    location = url_for("api.get_student", student_id=s.id, _external=False)
    return jsonify(s.to_dict()), 201, {"Location": location}


@api_bp.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    s = Student.query.get(student_id)
    if not s:
        return json_error("Student not found", status=404)

    data = request.get_json(silent=True)
    if data is None:
        return json_error("Invalid or missing JSON body", status=400)

    cleaned, errors = validate_student_payload(data, partial=True)
    if errors:
        return json_error("Validation failed", status=400, details=errors)

    if "student_id" in cleaned:
        other = Student.query.filter_by(student_id=cleaned["student_id"]).first()
        if other and other.id != s.id:
            return json_error("student_id already used by another student", status=409)
    if "email" in cleaned:
        other = Student.query.filter_by(email=cleaned["email"]).first()
        if other and other.id != s.id:
            return json_error("email already used by another student", status=409)

    try:
        s.update_from_dict(cleaned)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        current_app.logger.exception("Integrity error updating student")
        return json_error("Database integrity error", status=409)
    except Exception:
        db.session.rollback()
        current_app.logger.exception("Error updating student")
        return json_error("Internal server error", status=500)

    return jsonify(s.to_dict()), 200


@api_bp.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    s = Student.query.get(student_id)
    if not s:
        return json_error("Student not found", status=404)
    try:
        db.session.delete(s)
        db.session.commit()
    except Exception:
        db.session.rollback()
        current_app.logger.exception("Failed to delete student")
        return json_error("Internal server error", status=500)
    return "", 204


@api_bp.app_errorhandler(400)
def handle_400(err):
    return json_error("Bad request", status=400)


@api_bp.app_errorhandler(404)
def handle_404(err):
    return json_error("Not found", status=404)


@api_bp.app_errorhandler(500)
def handle_500(err):
    return json_error("Internal server error", status=500)
