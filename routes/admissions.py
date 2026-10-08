from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models.admission import Admission
from models import db

admissions_bp = Blueprint('admissions', __name__)

@admissions_bp.before_request
@login_required
def require_login():
    pass

@admissions_bp.route('/')
def list_admissions():
    search = request.args.get('search', '')
    if search:
        admissions = Admission.query.filter(Admission.name.ilike(f'%{search}%')).all()
    else:
        admissions = Admission.query.all()
    return render_template('admin/admissions.html', admissions=admissions, search=search)

@admissions_bp.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    admission = Admission.query.get_or_404(id)
    data = request.json
    admission.status = data.get('status')
    db.session.commit()
    return jsonify({'status': 'success'})

@admissions_bp.route('/delete/<int:id>', methods=['POST'])
def delete_admission(id):
    admission = Admission.query.get_or_404(id)
    db.session.delete(admission)
    db.session.commit()
    return jsonify({'status': 'success'})
