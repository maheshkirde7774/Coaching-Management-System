from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .course import Course
from .student import Student
from .admission import Admission
from .attendance import Attendance
from .fee import Fee
from .notice import Notice
