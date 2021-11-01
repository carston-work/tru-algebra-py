from datetime import datetime
from app import db, login_manager
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __init__(self, username, first, last, password, role='User'):
        self.username = username
        self.first_name = first
        self.last_name = last
        self.password = generate_password_hash(password)
        self.role = role
    
    _teach = db.relationship('Teacher', uselist=False, backref='user', lazy=True)
    _student = db.relationship('Student', uselist=False, backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username} {self.role}>'

    def get_id(self):
        return self.user_id


class Student(db.Model):

    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=True)

    def __init__(self, username, first, last, password, class_id=None):
        user = User(username, first, last, password, role="student")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.user_id
        self.class_id = class_id

    performances = db.relationship("Performance", backref="student", lazy=True)


class Teacher(db.Model):

    __tablename__ = "teachers"

    teacher_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    title = db.Column(db.String(10), nullable=True)

    def __init__(self, username, first, last, password, title):
        user = User(username, first, last, password, role="teacher")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.user_id
        self.title = title

    classes = db.relationship("Class", backref="teacher", lazy=True)
    equations = db.relationship("Equation", backref="creator", lazy=True)


class Class(db.Model):

    __tablename__ = 'classes'

    class_id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))
    class_name = db.Column(db.String(30), nullable=False)

    def __init__(self, teacher_id, class_name):
        self.teacher_id = teacher_id
        self.class_name = class_name

    
    students = db.relationship("Student", backref="classroom", lazy=True)
    assignments = db.relationship("Assignment", backref="classroom", lazy=True)


class Equation(db.Model):

    __tablename__ = "equations"

    equation_id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=False)
    lhs = db.Column(db.String(128), nullable=False)
    rhs = db.Column(db.String(128), nullable=False)

    def __init__(self, creator_id, lhs, rhs):
        self.creator_id = creator_id
        self.lhs = lhs
        self.rhs = rhs

    performances = db.relationship("Performance", backref='equation', lazy=True)
    assignments = db.relationship("Assignment", backref='equation', lazy=True)


class Performance(db.Model):

    __tablename__ = 'performances'

    performance_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    equation_id = db.Column(db.Integer, db.ForeignKey('equations.equation_id'), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    hints = db.Column(db.Integer)
    attempt = db.Column(db.Integer)
    diff_rating = db.Column(db.Integer)

    def __init__(self, student_id, equation_id, start_time=datetime.now, end_time=datetime.now, hints=0, attempt=1, diff_rating=0):
        self.student_id = student_id
        self.equation_id = equation_id
        if isinstance(start_time, type(callable)):
            self.start_time = start_time()
        else:
            self.start_time = start_time
        if isinstance(end_time, type(callable)):
            self.end_time = end_time()
        else:
            self.end_time = end_time
        self.hints = hints
        self.attempt = attempt 
        self.diff_rating = diff_rating


class Assignment(db.Model):

    __tablename__ = 'assignments'

    assignment_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)
    equation_id = db.Column(db.Integer, db.ForeignKey('equations.equation_id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, class_id, equation_id, due_date):
        self.class_id = class_id
        self.equation_id = equation_id
        self.due_date = datetime.strptime(due_date, '%Y-%m-%d%H:%M')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
