from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required
from models.notice import Notice
from models import db
from datetime import datetime

notices_bp = Blueprint('notices', __name__)

@notices_bp.before_request
@login_required
def require_login():
    pass

@notices_bp.route('/')
def list_notices():
    notices = Notice.query.order_by(Notice.date.desc()).all()
    return render_template('admin/notices.html', notices=notices)

@notices_bp.route('/add', methods=['POST'])
def add_notice():
    data = request.form
    date_val = datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else datetime.now().date()
    
    notice = Notice(
        title=data.get('title'),
        description=data.get('description'),
        date=date_val,
        category=data.get('category'),
        priority=data.get('priority'),
        is_published=True if data.get('is_published') else False
    )
    db.session.add(notice)
    db.session.commit()
    return redirect(url_for('notices.list_notices'))

@notices_bp.route('/delete/<int:id>', methods=['POST'])
def delete_notice(id):
    notice = Notice.query.get_or_404(id)
    db.session.delete(notice)
    db.session.commit()
    return jsonify({'status': 'success'})

@notices_bp.route('/toggle/<int:id>', methods=['POST'])
def toggle_notice(id):
    notice = Notice.query.get_or_404(id)
    notice.is_published = not notice.is_published
    db.session.commit()
    return jsonify({'status': 'success'})
