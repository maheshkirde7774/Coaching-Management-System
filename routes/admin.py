from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required
from models.student import Student
from models.course import Course
from models.admission import Admission
from models.fee import Fee
from models.attendance import Attendance
from models import db
from sqlalchemy import func
from datetime import datetime, timezone

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def require_login():
    pass

@admin_bp.route('/')
def dashboard():
    total_students = Student.query.count()
    total_courses = Course.query.count()
    pending_admissions = Admission.query.filter_by(status='Pending').count()
    
    total_fees_collected = db.session.query(func.sum(Fee.amount_paid)).scalar() or 0
    
    today = datetime.now(timezone.utc).date()
    todays_attendance = Attendance.query.filter_by(date=today, status='Present').count()
    
    return render_template('admin/dashboard.html',
                           total_students=total_students,
                           total_courses=total_courses,
                           pending_admissions=pending_admissions,
                           total_fees_collected=total_fees_collected,
                           todays_attendance=todays_attendance)

@admin_bp.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('admin/courses.html', courses=all_courses)

@admin_bp.route('/courses/add', methods=['POST'])
def add_course():
    data = request.form
    course = Course(
        name=data.get('name'),
        description=data.get('description'),
        duration=data.get('duration'),
        fees=data.get('fees'),
        eligibility=data.get('eligibility'),
        subjects=data.get('subjects')
    )
    db.session.add(course)
    db.session.commit()
    return redirect(url_for('admin.courses'))

@admin_bp.route('/courses/delete/<int:id>', methods=['POST'])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'status': 'success'})
