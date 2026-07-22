from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object here and initialize from app
db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    course = db.Column(db.String(120))
    year = db.Column(db.Integer)

    def __repr__(self):
        return f"<Student {self.name} ({self.email})>"
