# Smart Agriculture Management System

A Flask project with 45 database tables, login, CRUD pages and a dark glass UI.

## Setup

Windows:

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python run.py

Mac / Linux:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python run.py

Open http://127.0.0.1:5000 in the browser, register an account, then log in.
The SQLite database (all 45 tables) is created automatically on first run.

## Structure

- app/__init__.py : application factory
- app/models.py : all database models
- app/forms.py : WTForms classes
- app/auth.py, app/dashboard.py, app/crud.py : blueprints
- app/templates : Jinja2 templates
- app/static/style.css : styling
