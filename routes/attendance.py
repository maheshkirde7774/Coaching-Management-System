from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models.attendance import Attendance
from models.course import Course
from models.student import Student
from models import db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.before_request
@login_required
def require_login():
    pass

@attendance_bp.route('/', methods=['GET'])
def list_attendance():
    courses = Course.query.all()
    course_id = request.args.get('course_id')
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    students = []
    attendances = {}
    if course_id:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        students = Student.query.filter_by(course_id=course_id, status='Active').all()
        att_records = Attendance.query.filter_by(course_id=course_id, date=date_obj).all()
        for a in att_records:
            attendances[a.student_id] = a.status

    return render_template('admin/attendance.html', courses=courses, students=students, 
                           course_id=int(course_id) if course_id else None, 
                           date=date_str, attendances=attendances)

@attendance_bp.route('/mark', methods=['POST'])
def mark_attendance():
    data = request.json
    course_id = data.get('course_id')
    date_str = data.get('date')
    student_id = data.get('student_id')
    status = data.get('status')
    
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    att = Attendance.query.filter_by(course_id=course_id, date=date_obj, student_id=student_id).first()
    if att:
        att.status = status
    else:
        att = Attendance(course_id=course_id, date=date_obj, student_id=student_id, status=status)
        db.session.add(att)
    
    db.session.commit()
    return jsonify({'status': 'success'})
