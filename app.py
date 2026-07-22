import re
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student
from sqlalchemy.exc import IntegrityError

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'  # change for production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Homepage: render index.html (list of students)
    @app.route('/')
    def index():
        students = Student.query.order_by(Student.id.desc()).all()
        return render_template('index.html', students=students)

    # View all students page (alternative route)
    @app.route('/students')
    def students_view():
        students = Student.query.order_by(Student.id.desc()).all()
        return render_template('students.html', students=students)

    # Add student (GET shows form, POST stores in DB)
    @app.route('/add', methods=['GET', 'POST'])
    def add():
        if request.method == 'POST':
            # Collect form data
            student_id = request.form.get('student_id', '').strip()
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            age = request.form.get('age', '').strip()
            marks_raw = request.form.get('marks', '').strip()

            # Validation
            errors = []
            if not student_id:
                errors.append('Student ID is required')
            if not name:
                errors.append('Name is required')
            if not email:
                errors.append('Email is required')
            elif not EMAIL_RE.match(email):
                errors.append('Invalid email format')

            age_val = None
            if age:
                try:
                    age_val = int(age)
                    if age_val < 0:
                        errors.append('Age must be non-negative')
                except ValueError:
                    errors.append('Age must be a number')

            # Parse marks (comma separated)
            marks_list = []
            if marks_raw:
                parts = [p.strip() for p in marks_raw.split(',') if p.strip()]
                for i, p in enumerate(parts):
                    try:
                        marks_list.append(float(p))
                    except ValueError:
                        errors.append(f"Mark #{i+1} is not a valid number")

            # Check uniqueness
            if Student.query.filter_by(student_id=student_id).first():
                errors.append('Student ID already exists')
            if Student.query.filter_by(email=email).first():
                errors.append('Email already exists')

            if errors:
                for e in errors:
                    flash(e, 'danger')
                # Re-render form with previously entered values
                form_data = {
                    'student_id': student_id,
                    'name': name,
                    'email': email,
                    'age': age,
                    'marks': marks_raw,
                }
                return render_template('form.html', action='Add', student=form_data), 400

            # Create student
            try:
                s = Student(student_id=student_id, name=name, age=age_val, email=email)
                s.marks = marks_list
                db.session.add(s)
                db.session.commit()
                flash('Student added successfully.', 'success')
                return redirect(url_for('students_view'))
            except IntegrityError:
                db.session.rollback()
                flash('Database integrity error while creating the student.', 'danger')
                return render_template('form.html', action='Add', student=request.form), 500
            except Exception:
                db.session.rollback()
                app.logger.exception('Error creating student')
                flash('An internal error occurred while adding the student.', 'danger')
                return render_template('form.html', action='Add', student=request.form), 500

        # GET
        return render_template('form.html', action='Add')

    # View single student
    @app.route('/student/<int:student_id>')
    def view(student_id):
        s = Student.query.get_or_404(student_id)
        return render_template('view.html', student=s)

    # Delete student
    @app.route('/delete/<int:student_id>', methods=['POST'])
    def delete(student_id):
        s = Student.query.get_or_404(student_id)
        try:
            db.session.delete(s)
            db.session.commit()
            flash('Student deleted.', 'success')
        except Exception:
            db.session.rollback()
            app.logger.exception('Failed to delete student')
            flash('Failed to delete student.', 'danger')
        return redirect(url_for('students_view'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
