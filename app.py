from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'  # change for production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Routes
    @app.route('/')
    def index():
        students = Student.query.order_by(Student.id.desc()).all()
        return render_template('index.html', students=students)

    @app.route('/student/<int:student_id>')
    def view(student_id):
        student = Student.query.get_or_404(student_id)
        return render_template('view.html', student=student)

    @app.route('/add', methods=['GET', 'POST'])
    def add():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            course = request.form.get('course', '').strip()
            year = request.form.get('year', '').strip()

            if not name or not email:
                flash('Name and email are required.', 'danger')
                return render_template('form.html', action='Add', student=request.form)

            if Student.query.filter_by(email=email).first():
                flash('A student with that email already exists.', 'danger')
                return render_template('form.html', action='Add', student=request.form)

            try:
                year_val = int(year) if year else None
            except ValueError:
                flash('Year must be a number.', 'danger')
                return render_template('form.html', action='Add', student=request.form)

            s = Student(name=name, email=email, course=course, year=year_val)
            try:
                db.session.add(s)
                db.session.commit()
                flash('Student added successfully.', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                app.logger.exception('Failed to add student')
                flash('An error occurred.', 'danger')
                return render_template('form.html', action='Add', student=request.form)

        return render_template('form.html', action='Add')

    @app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
    def edit(student_id):
        student = Student.query.get_or_404(student_id)
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            course = request.form.get('course', '').strip()
            year = request.form.get('year', '').strip()

            if not name or not email:
                flash('Name and email are required.', 'danger')
                return render_template('form.html', action='Edit', student=request.form)

            other = Student.query.filter_by(email=email).first()
            if other and other.id != student.id:
                flash('Another student with that email already exists.', 'danger')
                return render_template('form.html', action='Edit', student=student)

            try:
                year_val = int(year) if year else None
            except ValueError:
                flash('Year must be a number.', 'danger')
                return render_template('form.html', action='Edit', student=student)

            student.name = name
            student.email = email
            student.course = course
            student.year = year_val
            try:
                db.session.commit()
                flash('Student updated successfully.', 'success')
                return redirect(url_for('index'))
            except Exception:
                db.session.rollback()
                app.logger.exception('Failed to update student')
                flash('An error occurred.', 'danger')
                return render_template('form.html', action='Edit', student=student)

        return render_template('form.html', action='Edit', student=student)

    @app.route('/delete/<int:student_id>', methods=['POST'])
    def delete(student_id):
        student = Student.query.get_or_404(student_id)
        try:
            db.session.delete(student)
            db.session.commit()
            flash('Student deleted.', 'success')
        except Exception:
            db.session.rollback()
            app.logger.exception('Failed to delete student')
            flash('Failed to delete student.', 'danger')
        return redirect(url_for('index'))

    # Error handlers
    @app.errorhandler(404)
    def not_found(err):
        return render_template('base.html', content='<h3>404 - Not Found</h3>'), 404

    @app.errorhandler(500)
    def internal_error(err):
        return render_template('base.html', content='<h3>500 - Server Error</h3>'), 500

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(debug=True)
