from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user
from flask_login.utils import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app.auth.forms import LoginForm, RegistrationForm
from app.models import Student, Teacher, User
from app import db

auth = Blueprint('auth', __name__, template_folder="templates")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash("That username is already registered to an account")
            return render_template('register.html', form=form)
        else:
            if form.role.data == '1':
                new_teacher = Teacher(form.username.data, form.first.data, form.last.data, form.password.data, form.title.data)
                db.session.add(new_teacher)
                db.session.commit()
                login_user(new_teacher.user)
            if form.role.data == '2':
                new_student = Student(form.username.data, form.first.data, form.last.data, form.password.data)
                db.session.add(new_student)
                db.session.commit()
                login_user(new_student.user)
        return redirect(url_for('users.profile'))


    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                if request.args.get('next'):
                    return redirect(request.args['next'])
                return redirect(url_for('users.profile'))
            else:
                flash("Password is incorrect")
        else:
            flash("That username does not exist. Would you like to register?")

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))