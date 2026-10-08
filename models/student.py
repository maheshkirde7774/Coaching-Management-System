from models import db
from datetime import datetime, timezone

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    admission_date = db.Column(db.Date)
    parent_name = db.Column(db.String(100))
    parent_phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Active') # Active, Inactive, Alumni
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    attendances = db.relationship('Attendance', backref='student_ref', lazy=True, cascade="all, delete-orphan")
    fees = db.relationship('Fee', backref='student_ref', lazy=True, cascade="all, delete-orphan")
