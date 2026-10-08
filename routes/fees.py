from flask import Blueprint, render_template, request, jsonify, redirect
from flask_login import login_required
from models.fee import Fee
from models.student import Student
from models import db
from sqlalchemy import func

fees_bp = Blueprint('fees', __name__)

@fees_bp.before_request
@login_required
def require_login():
    pass

@fees_bp.route('/')
def list_fees():
    search = request.args.get('search', '')
    if search:
        fees = Fee.query.join(Student).filter(Student.name.ilike(f'%{search}%')).all()
    else:
        fees = Fee.query.all()
    
    students = Student.query.filter_by(status='Active').all()
    
    # Calculate student total paid
    student_stats = []
    for s in students:
        paid = db.session.query(func.sum(Fee.amount_paid)).filter_by(student_id=s.id).scalar() or 0
        total = s.course_ref.fees if s.course_ref else 0
        rem = float(total) - float(paid)
        student_stats.append({
            'student': s,
            'total': total,
            'paid': paid,
            'rem': rem
        })
        
    return render_template('admin/fees.html', fees=fees, search=search, students=students, student_stats=student_stats)

@fees_bp.route('/add', methods=['POST'])
def add_fee():
    data = request.form
    fee = Fee(
        student_id=data.get('student_id'),
        total_fees=data.get('total_fees'),
        amount_paid=data.get('amount_paid'),
        payment_method=data.get('payment_method'),
        transaction_id=data.get('transaction_id')
    )
    rem = float(fee.total_fees) - float(fee.amount_paid)
    if rem <= 0:
        fee.status = 'Paid'
    elif float(fee.amount_paid) > 0:
        fee.status = 'Partial'
    else:
        fee.status = 'Pending'
        
    db.session.add(fee)
    db.session.commit()
    return redirect('/admin/fees/')

@fees_bp.route('/delete/<int:id>', methods=['POST'])
def delete_fee(id):
    fee = Fee.query.get_or_404(id)
    db.session.delete(fee)
    db.session.commit()
    return jsonify({'status': 'success'})
