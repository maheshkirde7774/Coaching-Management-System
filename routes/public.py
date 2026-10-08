from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from models.course import Course
from models.notice import Notice
from models.admission import Admission
from models import db
from datetime import datetime, timezone
import random
import string

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    popular_courses = Course.query.limit(3).all()
    notices = Notice.query.filter_by(is_published=True).order_by(Notice.date.desc()).limit(5).all()
    return render_template('home.html', courses=popular_courses, notices=notices)

@public_bp.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

@public_bp.route('/admission', methods=['GET', 'POST'])
def admission():
    courses = Course.query.all()
    if request.method == 'POST':
        data = request.form
        
        # Generate Application ID
        prefix = "APP-" + str(datetime.now().year) + "-"
        rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        app_id = prefix + rand_str
        
        dob_date = datetime.strptime(data.get('dob'), '%Y-%m-%d').date()
        
        new_app = Admission(
            application_id=app_id,
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            dob=dob_date,
            gender=data.get('gender'),
            address=data.get('address'),
            parent_name=data.get('parent_name'),
            parent_phone=data.get('parent_phone'),
            course_id=data.get('course_id'),
            previous_qualification=data.get('previous_qualification'),
            percentage=float(data.get('percentage')) if data.get('percentage') else 0.0
        )
        db.session.add(new_app)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"status": "success", "message": "Application submitted successfully!", "app_id": app_id})
        
        return render_template('admission.html', courses=courses, success=True, app_id=app_id)
        
    return render_template('admission.html', courses=courses)
