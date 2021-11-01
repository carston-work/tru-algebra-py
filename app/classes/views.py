from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import current_user
from flask_login.utils import login_required
from app.classes.forms import ClassForm, ClassSearchForm
from app.models import Class, User, Teacher, Student, Equation, Assignment
from app import db
 

classes = Blueprint('classes', __name__, template_folder="templates")


@classes.route('/add_class/<teacher_id>', methods=["GET", "POST"])
def add_class(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if teacher.user.user_id == current_user.user_id:
        form = ClassForm()

        if form.validate_on_submit():
            class_name = form.class_name.data
            cls = Class.query.filter(Class.class_name==class_name, Class.teacher_id==teacher_id).first()
            if cls:
                flash(f"You already have a class named {class_name}.")
                return render_template('add_class.html', form=form)
            else:
                new_class = Class(teacher_id, class_name)
                db.session.add(new_class)
                db.session.commit()
                return redirect(url_for('classes.view', class_id=new_class.class_id))

        return render_template('add_class.html', form=form)
    
    else:
        flash("you do not have access to that page")
        return redirect(url_for('main.home'))


@classes.route('/view/<class_id>')
def view(class_id):
    cls = Class.query.get(class_id)
    if not cls:
        flash("That class does not exist")
        return redirect(url_for('main.home'))    
    if cls.teacher.user.user_id != current_user.user_id:
        flash("You do not have permission to view this page")
        return redirect(url_for('main.home'))
    else:
        return render_template('view.html', my_class=cls)


@classes.route('/search', methods=['GET', "POST"])
def search():
    form = ClassSearchForm()
    teachers = None
    if form.validate_on_submit():
        teachers = None
        try:
            if form.teacher_first_name.data:
                teachers = Teacher.query.filter(Teacher.user_id==User.query.filter_by(last_name=form.teacher_last_name.data).first().user_id, Teacher.user_id==User.query.filter_by(first_name=form.teacher_first_name.data).first().user_id)
            else:
                teachers = Teacher.query.filter(Teacher.user_id==User.query.filter_by(last_name=form.teacher_last_name.data).first().user_id)
        except:
            flash("Your search found 0 results")

    return render_template('search.html', form=form, teachers=teachers)


@classes.route('/add_student/<class_id>')
@login_required
def add_student(class_id):
    student = Student.query.filter_by(user_id=current_user.user_id).first()
    my_class = Class.query.get(class_id)
    if my_class:
        if current_user.role == 'teacher' or not student.classroom:
            student.class_id = class_id
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('users.profile'))
        else: 
            flash("You do not have permission to perform that action.")
            return redirect(url_for('classes.search'))
            
    else:
        flash("Invalid action")
        return redirect(url_for('classes.search'))


@classes.route('/remove_student/<student_id>')
@login_required
def remove_student(student_id):
    if current_user.role == 'student':
        flash("You are not authorized to perform that action.")
        return redirect(url_for("main.home"))
    elif current_user.role == 'teacher':
        student = Student.query.get(student_id)
        teacher = Teacher.query.filter_by(user_id=current_user.user_id).first()
        if student.classroom in teacher.classes:
            my_class_id = student.class_id
            student.class_id = None
            db.session.commit()
            return redirect(url_for('classes.view', class_id=my_class_id))
        else:
            flash('You are not authorized to perform that action.')
            return redirect(url_for('users.profile'))



