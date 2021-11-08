from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user
from flask_login.utils import login_required
from sqlalchemy import desc
from app.models import Assignment, Student, Teacher, Performance
from app import db
from datetime import datetime

app = current_app
users = Blueprint('users', __name__, template_folder="templates")

def check_perfs(elem):
    student = Student.query.filter_by(user_id=current_user.user_id).first()
    return elem.student_id == student.student_id

@users.route('/profile')
@login_required
def profile():
    if current_user.role == 'student':
        student = Student.query.filter_by(user_id=current_user.user_id).first()
        if student.classroom:
            better_info = Assignment.query.filter(Assignment.class_id==student.class_id).order_by(desc(Assignment.due_date))
            my_student_perfs = []
            for assignment in better_info:
                perfs = filter(check_perfs,assignment.equation.performances)
                my_student_perfs.append(list(perfs))
            return render_template('profile.html', student=student, today=datetime.now, better_info=better_info, my_student_perfs=my_student_perfs)

        return render_template('profile.html', student=student)

    elif current_user.role == 'teacher':
        teacher = Teacher.query.filter_by(user_id=current_user.user_id).first()
        return render_template('profile.html', teacher=teacher)

@users.route('/stats/<user_id>')
@login_required
def stats(user_id):
    student = Student.query.filter_by(user_id=user_id).first()
    if current_user.role == 'student':
        if int(user_id) != current_user.user_id:
            flash("You are not authorized to view that information")
            return redirect(url_for("main.home"))
    elif current_user.role == 'teacher':
        teacher = Teacher.query.filter_by(user_id=current_user.user_id).first()
        if student.classroom not in teacher.classes:
            flash("You are not authorized to view that information")
            return redirect(url_for("main.home"))
    stats = db.engine.execute(f'''
    SELECT student_id, SUM(hints) as "total_hints",
    ROUND(AVG(hints),2) as "avg_hints", AVG(end_time - start_time) as "avg_time",
    ROUND(AVG(diff_rating),2) as "avg_diff_rating"
    FROM performances
    WHERE student_id={student.student_id}
    GROUP BY student_id;
    ''').first()
    avg_time = str(stats.avg_time)
    _, min, sec = avg_time.split(':')
    avg_time = f'{min} min {round(int(sec), 2)} sec'
    return render_template('stats.html', stats=stats, classroom=student.classroom, avg_time=avg_time)