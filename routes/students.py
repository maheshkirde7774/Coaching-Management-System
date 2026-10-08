from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required
from models.student import Student
from models.course import Course
from models import db
from datetime import datetime

students_bp = Blueprint('students', __name__)

@students_bp.before_request
@login_required
def require_login():
    pass

@students_bp.route('/')
def list_students():
    search = request.args.get('search', '')
    if search:
        students = Student.query.filter(Student.name.ilike(f'%{search}%')).all()
    else:
        students = Student.query.all()
    return render_template('admin/students.html', students=students, search=search)

@students_bp.route('/add', methods=['GET', 'POST'])
def add_student():
    courses = Course.query.all()
    if request.method == 'POST':
        prefix = "STU-" + str(datetime.now().year) + "-"
        count = Student.query.count() + 1
        stu_id = prefix + f"{count:04d}"
        
        dob_date = datetime.strptime(request.form.get('dob'), '%Y-%m-%d').date()
        adm_date = datetime.strptime(request.form.get('admission_date'), '%Y-%m-%d').date() if request.form.get('admission_date') else datetime.now().date()
        
        student = Student(
            student_id=stu_id,
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            dob=dob_date,
            gender=request.form.get('gender'),
            address=request.form.get('address'),
            course_id=request.form.get('course_id'),
            admission_date=adm_date,
            parent_name=request.form.get('parent_name'),
            parent_phone=request.form.get('parent_phone'),
            status=request.form.get('status', 'Active')
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('students.list_students'))
    return render_template('admin/student_form.html', courses=courses, student=None)

@students_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    courses = Course.query.all()
    if request.method == 'POST':
        student.name = request.form.get('name')
        student.email = request.form.get('email')
        student.phone = request.form.get('phone')
        student.dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d').date()
        student.gender = request.form.get('gender')
        student.address = request.form.get('address')
        student.course_id = request.form.get('course_id')
        if request.form.get('admission_date'):
            student.admission_date = datetime.strptime(request.form.get('admission_date'), '%Y-%m-%d').date()
        student.parent_name = request.form.get('parent_name')
        student.parent_phone = request.form.get('parent_phone')
        student.status = request.form.get('status')
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('students.list_students'))
    return render_template('admin/student_form.html', courses=courses, student=student)

@students_bp.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'status': 'success'})
