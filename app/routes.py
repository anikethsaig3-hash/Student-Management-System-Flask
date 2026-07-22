from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash
from . import db
from .models import Student


@app.route('/')
def index():
    return redirect(url_for('list_students'))


@app.route('/students')
def list_students():
    students = Student.query.order_by(Student.id.desc()).all()
    return render_template('students.html', students=students)


@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()
        year = request.form.get('year')

        # Basic validation
        if not name or not email:
            flash('Name and email are required.', 'danger')
            return render_template('add_student.html', form=request.form)

        # Prevent duplicate emails
        if Student.query.filter_by(email=email).first():
            flash('A student with that email already exists.', 'danger')
            return render_template('add_student.html', form=request.form)

        try:
            year_val = int(year) if year else None
        except ValueError:
            flash('Year must be a number.', 'danger')
            return render_template('add_student.html', form=request.form)

        student = Student(name=name, email=email, course=course, year=year_val)
        try:
            db.session.add(student)
            db.session.commit()
            flash('Student added successfully.', 'success')
            return redirect(url_for('list_students'))
        except Exception as e:
            db.session.rollback()
            app.logger.exception('Failed to add student')
            flash('An error occurred while adding the student.', 'danger')
            return render_template('add_student.html', form=request.form)

    return render_template('add_student.html')


@app.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()
        year = request.form.get('year')

        if not name or not email:
            flash('Name and email are required.', 'danger')
            return render_template('edit_student.html', student=student)

        # Check for email conflict
        other = Student.query.filter_by(email=email).first()
        if other and other.id != student.id:
            flash('Another student with that email already exists.', 'danger')
            return render_template('edit_student.html', student=student)

        try:
            year_val = int(year) if year else None
        except ValueError:
            flash('Year must be a number.', 'danger')
            return render_template('edit_student.html', student=student)

        student.name = name
        student.email = email
        student.course = course
        student.year = year_val

        try:
            db.session.commit()
            flash('Student updated successfully.', 'success')
            return redirect(url_for('list_students'))
        except Exception:
            db.session.rollback()
            app.logger.exception('Failed to update student')
            flash('An error occurred while updating the student.', 'danger')
            return render_template('edit_student.html', student=student)

    return render_template('edit_student.html', student=student)


@app.route('/students/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted.', 'success')
    except Exception:
        db.session.rollback()
        app.logger.exception('Failed to delete student')
        flash('Failed to delete student.', 'danger')
    return redirect(url_for('list_students'))


@app.route('/students/<int:student_id>')
def view_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('view_student.html', student=student)
