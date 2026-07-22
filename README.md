# Student Management System (Flask + SQLite)

A simple, professional Student Management System built with Flask, SQLite and SQLAlchemy. It provides a responsive Bootstrap frontend and a JSON REST API for managing student records (create, read, update, delete). The project is designed as a learning/demo app with a clear folder structure and sensible defaults for quick local development.

---

## Repository language composition
These values were provided by the repository owner and recorded here for reference.

- Python — 53.7%
- HTML — 43.5%
- JavaScript — 2.4%
- CSS — 0.4%

Note: GitHub computes a language breakdown automatically (Linguist) based on file extensions and byte counts. The values above reflect the composition supplied on 2026-07-22 and are included here for clarity; the live GitHub language bar may differ slightly as files change.

---

## Table of contents
- Project Overview
- Features
- Folder structure
- Installation
- Running the app (development)
- Configuration
- API Documentation (quick)
- Frontend pages
- Screenshots
- Next steps / Recommendations
- Contributing
- License

---

## Project overview
This application allows you to:
- Register students with Student ID, name, age and email.
- Store and display student marks (stored as JSON), compute average and grade.
- View, edit and delete student records via frontend pages and via a RESTful JSON API.
- Provide a responsive, modern UI built with Bootstrap and custom CSS.

Technologies:
- Python, Flask
- SQLite (local file `students.db`)
- SQLAlchemy ORM
- Jinja2 templates
- Bootstrap 5 + custom responsive CSS

---

## Features
- Register students (Student ID, Name, Age, Email)
- View all students in a responsive table
- Student detail view
- Delete student records
- Marks stored as JSON, automatic average and grade calculation
- REST API for programmatic access (`/api/students`)
- Validation (client-side + server-side) and error handling
- Responsive layout, modern dashboard styling, and accessible UX

---

## Folder structure
Root layout (key files and folders)

```
Student-Management-System-Flask/
├── app.py                   # Application shim (imports app package create_app)
├── run.py                   # Starts the application (dev)
├── app/                     # Package with application factory, models, and routes
│   ├── __init__.py          # create_app() and db object
│   ├── models.py            # SQLAlchemy models (Student)
│   └── routes.py            # Server-rendered HTML routes
├── api.py                   # REST API blueprint (registered at /api)
├── postman_collection.json  # Postman collection for API endpoints
├── requirements.txt
├── README.md
├── templates/               # Jinja2 templates (base, index, form, view, register, etc.)
└── static/
    ├── css/
    │   └── style.css
    └── js/
        ├── script.js
        └── form-validation.js
```

Notes:
- The SQLite database file `students.db` is created in the project root when the app first runs.
- The API blueprint is registered inside the application factory and is available at `/api` by default.

---

## Installation

1. Clone the repository
```bash
git clone https://github.com/anikethsaig3-hash/Student-Management-System-Flask.git
cd Student-Management-System-Flask
```

2. Create and activate a Python virtual environment

```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the app (development)

Start the Flask app (development mode):

```bash
python run.py
```

By default the app runs on:

```
http://127.0.0.1:5000
```

Pages:
- Home / Students list: `GET /` or `GET /students`
- Add student (form): `GET /add` (form posts to `/add`)
- Student detail: `GET /student/<id>`
- Register form: `GET /register`
- Delete student: `POST /delete/<id>`

API endpoints (if the API blueprint is registered at `/api`):
- List/create: `GET /api/students`, `POST /api/students`
- Retrieve/update/delete: `GET /api/students/<id>`, `PUT /api/students/<id>`, `DELETE /api/students/<id>`

---

## Configuration

The app uses a simple configuration in `app/__init__.py`. For production, change or provide these (recommended):

- `SECRET_KEY` — set a secure random value via environment variable:
```python
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
```

- To change the database file location:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////path/to/your/dbfile.db'
```

Consider using Flask-Migrate (Alembic) for production databases and schema evolution.

---

## API Documentation (quick)

Base URL (example): `http://127.0.0.1:5000/api`

All request/response bodies are JSON and the API returns appropriate status codes and JSON error objects on failure.

1) List students
- Method: GET
- URL: `/api/students`
- Response: `200 OK` — array of student objects

2) Get student
- Method: GET
- URL: `/api/students/<id>`
- Response: `200 OK` or `404 Not Found`

3) Create student
- Method: POST
- URL: `/api/students`
- Content-Type: `application/json`
- Body example:
```json
{
  "student_id": "S001",
  "name": "Alice",
  "email": "alice@example.com",
  "age": 20,
  "marks": [90, 85, 78]
}
```
- Success: `201 Created` (returns created student JSON and Location header)
- Validation errors: `400 Bad Request` with details array
- Uniqueness conflict: `409 Conflict`

4) Update student
- Method: PUT
- URL: `/api/students/<id>`
- Body example (partial update allowed):
```json
{
  "name": "Alice B.",
  "marks": [95, 92]
}
```
- Success: `200 OK`

5) Delete student
- Method: DELETE
- URL: `/api/students/<id>`
- Success: `204 No Content`

---

## Frontend pages

The project provides server-rendered pages using Jinja templates:
- `index.html` — Landing / students list
- `students.html` — All students listing
- `form.html` — Add / Edit form
- `view.html` — Student details
- `register.html` — Modern registration form (client-side + server-side validation)

Forms use:
- Bootstrap 5 for layout and components
- Client-side validation helper `static/js/form-validation.js`
- Server-side validation and flashing of errors/success via Flask's `flash()`.

---

## Screenshots

Add screenshots to this section to demonstrate UI. Example placeholders:

- Home / Dashboard
  ![Home Screenshot](screenshots/home.png)

- Add Student form
  ![Add Student Screenshot](screenshots/add-student.png)

- Students List (responsive table)
  ![Students List Screenshot](screenshots/students-list.png)

To include real screenshots:
1. Create a `screenshots/` folder in the repo root.
2. Save PNG/JPEG screenshots with the filenames used above (or update the README image paths).
3. Commit and push.

---

## Next steps & recommendations
- Add Flask-Migrate for database migrations (recommended for production).
- Use Flask-WTF for robust form handling and CSRF protection.
- Add authentication (Flask-Login or token-based) for protected operations.
- Add pagination, filtering, and server-side search for large datasets.
- Pin dependency versions in `requirements.txt` or add a lock file.
- Add unit and integration tests (pytest + test database).
- Add Dockerfile + docker-compose for reproducible deployments.
- Add OpenAPI/Swagger documentation and Postman collection.

---

## Contributing
Contributions are welcome. Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes with clear messages
4. Open a pull request describing the change

If you open issues, include steps to reproduce and the expected vs actual behavior.

---

## License
This project is provided under the MIT License. See LICENSE file for details (or add an appropriate LICENSE file to the repository).
