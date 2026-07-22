import json
from typing import List, Optional, Dict, Any

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # store marks as JSON-encoded text for SQLite portability
    _marks = db.Column("marks", db.Text, nullable=False, default="[]")
    average = db.Column(db.Float, nullable=True)
    grade = db.Column(db.String(4), nullable=True)

    def __repr__(self) -> str:
        return f"<Student id={self.id} student_id={self.student_id} name={self.name!r}>"

    #
    # Marks property (serialize/deserialize JSON)
    #
    @property
    def marks(self) -> List[float]:
        """Return marks as a list of numbers."""
        try:
            return json.loads(self._marks or "[]")
        except (TypeError, ValueError):
            return []

    @marks.setter
    def marks(self, value: Optional[List[float]]) -> None:
        """Set marks from a list (or None). Recomputes average & grade."""
        if value is None:
            value = []
        # Normalize values to float and filter non-numeric entries
        normalized = []
        for v in value:
            try:
                normalized.append(float(v))
            except (TypeError, ValueError):
                continue
        self._marks = json.dumps(normalized)
        self._compute_stats()

    def _compute_stats(self) -> None:
        """Compute average and grade based on current marks. Stores results on model."""
        marks = self.marks
        if marks:
            avg = float(sum(marks)) / len(marks)
            self.average = round(avg, 2)
            self.grade = self._grade_from_average(self.average)
        else:
            self.average = None
            self.grade = None

    @staticmethod
    def _grade_from_average(avg: float) -> str:
        """Simple grading scheme. Customize as needed."""
        if avg >= 90:
            return "A"
        if avg >= 80:
            return "B"
        if avg >= 70:
            return "C"
        if avg >= 60:
            return "D"
        return "F"

    #
    # Serialization helpers
    #
    def to_dict(self, include_private: bool = False) -> Dict[str, Any]:
        """
        Convert the model to a dict suitable for JSON serialization.
        - include_private: if True, includes internal fields like _marks (raw JSON string).
        """
        data = {
            "id": self.id,
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "marks": self.marks,
            "average": self.average,
            "grade": self.grade,
        }
        if include_private:
            data["_marks_raw"] = self._marks
        return data

    def to_json(self) -> str:
        """Return a JSON string representation (uses to_dict)."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """
        Create a Student instance from a dict. Does NOT add to session or commit.
        Expected keys: student_id, name, age, email, marks (list/iterable of numbers).
        """
        s = cls(
            student_id=data.get("student_id") or data.get("id") or "",
            name=data.get("name", ""),
            age=data.get("age"),
            email=data.get("email", ""),
        )
        # set marks via property to trigger stats computation
        s.marks = data.get("marks", [])
        return s

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """
        Update mutable fields from a dictionary and recompute stats if marks changed.
        Does not commit the session.
        """
        if "student_id" in data:
            self.student_id = data["student_id"]
        if "name" in data:
            self.name = data["name"]
        if "age" in data:
            self.age = data["age"]
        if "email" in data:
            self.email = data["email"]
        if "marks" in data:
            self.marks = data["marks"]
        else:
            # if other fields changed but marks not provided, leave marks/average/grade as-is
            pass
