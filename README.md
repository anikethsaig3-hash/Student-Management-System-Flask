# Student Management System (Flask + SQLite)

This project contains a minimal Student Management System built with Flask and SQLite using SQLAlchemy.

Files and structure
- app.py            # Main application (routes + app factory)
- models.py         # SQLAlchemy models and db object
- templates/        # Jinja2 templates (base, index, form, view)
- static/css/style.css
- static/js/script.js

Quickstart
1. Create a virtual environment and install deps

   python -m venv venv
   source venv/bin/activate  # macOS / Linux
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt

2. Run the app

   python app.py

3. Open http://127.0.0.1:5000

Notes
- The app uses a development SECRET_KEY. Replace it with a secure value for production.
- The SQLite database file `students.db` will be created in the project root on first run.
