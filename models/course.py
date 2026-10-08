from models import db
from datetime import datetime, timezone

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.String(50))
    fees = db.Column(db.Numeric(10, 2), nullable=False)
    eligibility = db.Column(db.String(200))
    subjects = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    students = db.relationship('Student', backref='course_ref', lazy=True)
    admissions = db.relationship('Admission', backref='course_ref', lazy=True)
