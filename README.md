# Coaching Management System

A complete, production-ready Coaching Institute Management platform built with Flask and PostgreSQL.

## Features
- Public website with courses and online admission.
- Admin authentication and secure dashboard.
- Student management (CRUD).
- Admission tracking (Approve/Reject).
- Attendance marking and history.
- Fee management with partial/full payment tracking.
- Notice board.
- Interactive charts using Chart.js.
- Responsive design with Bootstrap 5.

## Tech Stack
- **Backend:** Python 3, Flask, SQLAlchemy, Flask-Login, Flask-Migrate
- **Database:** PostgreSQL
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js

## Installation

1. Navigate to the project directory:
   ```bash
   cd coaching-management
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up PostgreSQL and create a database named `coaching_db`.
5. Create a `.env` file from `.env.example` and update credentials.
6. Initialize Database and Seed Data:
   ```bash
   python seed.py
   ```
7. Run the application:
   ```bash
   python app.py
   ```

## Admin Login
- Email: `admin@example.com`
- Password: `admin123`

## Deployment
For Render/Railway, ensure to set `DATABASE_URL` and `SECRET_KEY` in the environment variables, and use `gunicorn app:app` as the start command.




main cammands 
cd coaching-management
pip install -r requirements.txt
python seed.py
python app.py



gor github
cd .\coaching-management