from flask import Blueprint, redirect, render_template, flash, request
from flask.helpers import url_for
from flask_login import current_user, login_required
from app.assignments.forms import AssignmentFilter
from app.models import Assignment, Class, Teacher, Equation
from app import db

assignments = Blueprint('assignments', __name__, template_folder='templates')



@assignments.route('/add_assignment/<class_id>')
@login_required
def search_assignment(class_id):
    my_class = Class.query.get(class_id)
    equations = db.engine.execute('''
    SELECT eq.equation_id, eq.lhs as lhs, eq.rhs as rhs, ROUND(AVG(p.diff_rating), 2) as "difficulty"
    FROM equations as eq
    JOIN performances as p
    ON eq.equation_id = p.equation_id
    GROUP BY eq.equation_id
    ORDER BY "difficulty"''')
    form1 = AssignmentFilter()

    return render_template('search_assignments.html', my_class=my_class, form1=form1, equations=equations)


@assignments.route('/add_assignment/<class_id>/<equation_id>', methods=["GET", "POST"])
@login_required
def add_assignment(class_id, equation_id):
    teacher = Teacher.query.filter_by(user_id=current_user.user_id).first()
    if teacher:

        if request.method == "POST":
            date_time = request.form.get('due_date') + request.form.get('due_time')
            assign = Assignment(class_id, equation_id, date_time)
            db.session.add(assign)
            db.session.commit()
            flash("Assignment created")
            return redirect(url_for('assignments.search_assignment', class_id=class_id))
        
        my_class = Class.query.get(class_id)
        my_eq = Equation.query.get(equation_id)
        return render_template('add_assignment.html', my_equation=my_eq, my_class=my_class)
        
    else:
        flash("You do not have permission to view that page.")
        return redirect(url_for('main.home'))
