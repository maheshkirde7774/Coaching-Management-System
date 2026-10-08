from models import db
from datetime import datetime, timezone

class Admission(db.Model):
    __tablename__ = 'admissions'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)
    parent_name = db.Column(db.String(100))
    parent_phone = db.Column(db.String(20))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    previous_qualification = db.Column(db.String(100))
    percentage = db.Column(db.Numeric(5, 2))
    status = db.Column(db.String(20), default='Pending') # Pending, Approved, Rejected
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
