Student Management System (Flask + SQLite)

This repository contains a simple Student Management System built with Flask and SQLite using SQLAlchemy ORM. It includes a Bootstrap frontend with Jinja templates and basic CRUD operations for students.

Features
- List, add, edit, view, and delete students
- Flask backend with SQLAlchemy ORM
- SQLite database (students.db created in project root)
- Templates with Bootstrap for responsive UI
- Basic error handling (404, 500)

Getting started

1. Clone the repository

   git clone https://github.com/anikethsaig3-hash/Student-Management-System-Flask.git
   cd Student-Management-System-Flask

2. Create a virtual environment and install dependencies

   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   pip install -r requirements.txt

3. Run the app

   python run.py

4. Open your browser at http://127.0.0.1:5000

Notes
- The app uses a simple SECRET_KEY value for development. Replace it with a secure key for production.
- The SQLite database file `students.db` is created automatically on first run.

License
MIT
