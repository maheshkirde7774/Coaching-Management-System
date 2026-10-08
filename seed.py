from app import app, db
from models.user import User
from models.course import Course
from models.student import Student
from models.admission import Admission
from models.notice import Notice
from models.attendance import Attendance
from models.fee import Fee
from datetime import datetime, timedelta, timezone

def seed():
    with app.app_context():
        db.create_all()
        
        # Check if admin exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('admin123')
            db.session.add(admin)
            
        # Add Courses
        if not Course.query.first():
            courses = [
                Course(name='Web Development Bootcamp', description='Learn full-stack web development with Python and JavaScript.', duration='6 Months', fees=1500.00, eligibility='Basic programming knowledge', subjects='HTML, CSS, JS, Python, Flask'),
                Course(name='Data Science Masterclass', description='Master data analysis and machine learning.', duration='8 Months', fees=2000.00, eligibility='Mathematics background', subjects='Python, Pandas, ML, AI'),
                Course(name='UI/UX Design Course', description='Create stunning user interfaces.', duration='3 Months', fees=800.00, eligibility='Creative mindset', subjects='Figma, Adobe XD, Design Principles'),
                Course(name='Cloud Computing with AWS', description='Prepare for AWS certifications.', duration='4 Months', fees=1200.00, eligibility='IT basics', subjects='AWS EC2, S3, RDS, Lambda'),
                Course(name='Mobile App Development', description='Build apps for iOS and Android.', duration='5 Months', fees=1600.00, eligibility='Programming basics', subjects='Flutter, Dart, Firebase')
            ]
            db.session.add_all(courses)
            db.session.commit()

        course1 = Course.query.filter_by(name='Web Development Bootcamp').first()
        course2 = Course.query.filter_by(name='Data Science Masterclass').first()
        
        # Add Students
        if not Student.query.first():
            students = []
            for i in range(1, 16):
                c = course1 if i % 2 == 0 else course2
                s = Student(
                    student_id=f'STU-2026-{i:04d}',
                    name=f'Student {i}',
                    email=f'student{i}@example.com',
                    phone=f'123456789{i}',
                    dob=datetime.now().date() - timedelta(days=365*20),
                    gender='Male' if i % 2 == 0 else 'Female',
                    address=f'{i} Main St, City',
                    course_id=c.id,
                    admission_date=datetime.now().date(),
                    parent_name=f'Parent {i}',
                    parent_phone=f'987654321{i}',
                    status='Active'
                )
                students.append(s)
            db.session.add_all(students)
            db.session.commit()

        # Add Admissions
        if not Admission.query.first():
            admissions = []
            for i in range(1, 11):
                a = Admission(
                    application_id=f'APP-2026-{i:05d}',
                    name=f'Applicant {i}',
                    email=f'applicant{i}@example.com',
                    phone=f'55555555{i}',
                    dob=datetime.now().date() - timedelta(days=365*18),
                    gender='Male',
                    address=f'{i} Applicant Rd',
                    parent_name=f'Guardian {i}',
                    parent_phone=f'44444444{i}',
                    course_id=course1.id,
                    previous_qualification='High School',
                    percentage=85.5 + i,
                    status='Pending' if i % 3 == 0 else ('Approved' if i % 2 == 0 else 'Rejected')
                )
                admissions.append(a)
            db.session.add_all(admissions)
            db.session.commit()

        # Add Notices
        if not Notice.query.first():
            notices = [
                Notice(title='Semester Exams Schedule', description='The end of semester exams will begin from 15th Nov.', date=datetime.now().date(), category='Exam', priority='High'),
                Notice(title='Diwali Holiday', description='Institute will remain closed for Diwali on 23rd Oct.', date=datetime.now().date(), category='Holiday', priority='Normal'),
                Notice(title='New Batch Admissions', description='Admissions for Web Dev batch starting soon.', date=datetime.now().date(), category='Admission', priority='High'),
                Notice(title='Tech Seminar', description='Guest lecture on AI on Friday.', date=datetime.now().date(), category='Event', priority='Normal'),
                Notice(title='Library Update', description='New books added to the library.', date=datetime.now().date(), category='General', priority='Low'),
            ]
            db.session.add_all(notices)
            db.session.commit()

        # Add Fees & Attendance
        student1 = Student.query.first()
        if student1 and not Fee.query.first():
            fee = Fee(student_id=student1.id, total_fees=student1.course_ref.fees, amount_paid=500.0, payment_method='Credit Card', transaction_id='TXN123456', status='Partial')
            db.session.add(fee)
            
            att = Attendance(student_id=student1.id, course_id=student1.course_id, date=datetime.now().date(), status='Present')
            db.session.add(att)
            db.session.commit()
            
        print("Database seeded successfully! Admin credentials -> admin@example.com / admin123")

if __name__ == '__main__':
    seed()
