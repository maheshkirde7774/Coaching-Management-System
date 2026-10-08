from models import db
from datetime import datetime, timezone

class Fee(db.Model):
    __tablename__ = 'fees'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    total_fees = db.Column(db.Numeric(10, 2), nullable=False)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    payment_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    status = db.Column(db.String(20)) # Paid, Partial, Pending
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    @property
    def remaining_fees(self):
        return self.total_fees - self.amount_paid
