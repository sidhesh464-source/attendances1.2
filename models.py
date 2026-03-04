from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False) # e.g., Register No for students
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False) # 'student' or 'faculty'
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    
    # Common profile fields
    phone = db.Column(db.String(20))
    age = db.Column(db.Integer)
    dob = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    photo = db.Column(db.String(200), default='default.jpg') # Path to photo
    is_blocked = db.Column(db.Boolean, default=False)


    # Student specific
    father_name = db.Column(db.String(150))
    mother_name = db.Column(db.String(150))
    father_phone = db.Column(db.String(20))
    mother_phone = db.Column(db.String(20))

    # Faculty specific
    department = db.Column(db.String(100))
    date_of_join = db.Column(db.String(20))

class SchoolClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'), nullable=False)
    student = db.relationship('User', backref=db.backref('enrollments', lazy=True))
    school_class = db.relationship('SchoolClass', backref=db.backref('enrollments', lazy=True))

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False) # 'Present', 'Absent'
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # User who marked it

    student = db.relationship('User', foreign_keys=[student_id], backref=db.backref('attendance_records', lazy=True))
    school_class = db.relationship('SchoolClass', backref=db.backref('attendance_records', lazy=True))
    faculty = db.relationship('User', foreign_keys=[faculty_id])

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Target audience: 'student', 'faculty', 'both'
    recipient_type = db.Column(db.String(20), nullable=False) 
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', backref='sent_messages')
