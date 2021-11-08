from flask import Blueprint, url_for, render_template, redirect, request, session, current_app, jsonify, flash
from flask_login import current_user, login_required
from app import db
from app.equations.forms import DiffRating, NewEquation
from sqlalchemy import desc
from app.models import Equation, Performance, Student, Teacher
from sympy import Symbol, latex, expand, Rational, Pow, Add, Mul, together, preorder_traversal
from latex2sympy2 import latex2sympy
from datetime import datetime
import json


equations = Blueprint("equations", __name__, template_folder="templates")
x = Symbol('x')
app = current_app



def clean_up(latex_expr:str):
    return latex_expr.replace('\\left(-1\\right)', '-')

def _do_math(alg_expr):
    if alg_expr[-1] == 'x':
        do_math = alg_expr.replace('x', '*x')
        try:
            if isinstance(int(do_math[-3]), int):
                pass
        except:
            do_math = do_math.replace('*x', 'x')
    else:
        do_math = alg_expr
    return do_math

def check_complete():
    if session['lhs'] == '0' and session['rhs'] == '0':
        session['solved'] = True
        session['end_time'] = datetime.now()
    elif session['lhs'] == 'x' or session['rhs'] == 'x':
        lhs, rhs = latex2sympy(session['lhs']), latex2sympy(session['rhs'])
        if 'x' in session['lhs'] and 'x' in session['rhs']:
            session['solved'] = False
        elif (isinstance(lhs, Symbol) and (isinstance(rhs, Rational) or (isinstance(rhs, Mul) and x not in rhs.args))) or\
            (isinstance(rhs, Symbol) and (isinstance(lhs, Rational) or (isinstance(lhs, Mul) and x not in lhs.args))):
            session['lhs'], session['rhs'] = latex(expand(lhs)), latex(expand(rhs))
            session['solved'] = True
            session['end_time'] = datetime.now()
        else:
            session['solved'] = False
    else:
        session['solved'] = False
            

@equations.route('/check_solution')
def check_solution():
    if session.get('solved'):
        return jsonify(session['solved'])
    return jsonify(False)

@equations.route('/finished', methods=["POST"])
def finished():
    if session.get('hints'):
        hints = session['hints']
    else:
        hints = 0
    my_student = Student.query.filter_by(user_id=current_user.user_id).first()
    performance = Performance(my_student.student_id, session['eq_id'], session["start_time"], session['end_time'], hints, session.get('attempt'), request.form['diff'])
    db.session.add(performance)
    db.session.commit()
    return redirect(url_for('users.profile'))

session_attrs = ['lhs', 'rhs', 'hints', 'start_time', 'end_time', 'eq_id', 'attempt', 'undo', 'solved']

@equations.route('/solve/<equation_id>')
def solve(equation_id):
    for attr in session_attrs:
        if session.get(attr):
            session.pop(attr)
    session['undo'] = list()
    session['eq_id'] = equation_id
    if current_user.is_authenticated and current_user.role == "student":
        most_recent = Performance.query.filter_by(student_id=current_user._student.student_id, equation_id=equation_id).order_by(desc(Performance.attempt)).first()
        if most_recent:
            session['attempt'] = most_recent.attempt + 1
        else:
            session['attempt'] = 1
    session['start_time'] = datetime.now()
    form = DiffRating()
    equation = Equation.query.get(equation_id)
    session['lhs'], session['rhs'] = equation.lhs, equation.rhs
    return render_template('solve.html', equation=equation, form=form)

@equations.route('/add_sub')
def add_sub():
    session['undo'].append((session['lhs'], session['rhs']))
    do_math = _do_math(request.args['alg'])
    lhs, rhs = latex2sympy(session['lhs']), latex2sympy(session['rhs'])
    if do_math[-1] == 'x':
        lhs = Add(eval(do_math), lhs, evaluate=False)
        rhs = Add(eval(do_math), rhs, evaluate=False)
    else:
        lhs = Add(eval(do_math), lhs)
        rhs = Add(eval(do_math), rhs)
    session['lhs'], session['rhs'] = clean_up(latex(lhs)), clean_up(latex(rhs))
    check_complete()
    return_tuple = (session['lhs'], session['rhs'])
    return jsonify(return_tuple)

@equations.route('/multi')
def multi():
    session['undo'].append((clean_up(session['lhs']), clean_up(session['rhs'])))
    do_math = _do_math(request.args['alg'])
    lhs, rhs = latex2sympy(session['lhs']), latex2sympy(session['rhs'])
    if isinstance(lhs,Mul):
        lhs = Mul(eval(do_math), lhs)
    else:
        lhs = Mul(eval(do_math), lhs, evaluate=False)
    if isinstance(rhs,Mul):
        rhs = Mul(eval(do_math), rhs)
    else:
        rhs = Mul(eval(do_math), rhs, evaluate=False)
    session['lhs'], session['rhs'] = clean_up(latex(lhs)), clean_up(latex(rhs))
    check_complete()
    return_tuple = (session['lhs'], session['rhs'])
    return jsonify(return_tuple)

@equations.route('/div')
def div():
    session['undo'].append((clean_up(session['lhs']), clean_up(session['rhs'])))
    do_math = _do_math(request.args['alg'])
    lhs, rhs = latex2sympy(session['lhs']), latex2sympy(session['rhs'])
    if isinstance(lhs,Mul):
        lhs = Mul(lhs, Pow(eval(do_math), -1))
    else:
        lhs = Mul(lhs, Pow(eval(do_math), -1), evaluate=False)
    if isinstance(rhs,Mul):
        rhs = Mul(rhs, Pow(eval(do_math), -1))
    else:
        rhs = Mul(rhs, Pow(eval(do_math), -1), evaluate=False)
    session['lhs'], session['rhs'] = clean_up(latex(lhs)), clean_up(latex(rhs))
    check_complete()
    return_tuple = (session['lhs'], session['rhs'])
    return jsonify(return_tuple)

@equations.route('/distribute/<left_right>')
def distribute(left_right):
    session['undo'].append((session['lhs'], session['rhs']))
    if left_right == 'lhs':
        lhs = expand(latex2sympy(session['lhs']))
        session['lhs'] = clean_up(latex(lhs))
    elif left_right == 'rhs':
        rhs = expand(latex2sympy(session['rhs']))
        session['rhs'] = clean_up(latex(rhs))
    check_complete()
    return_tuple = (session['lhs'], session['rhs'])
    return jsonify(return_tuple)

@equations.route('/combine/<left_right>')
def combine(left_right):
    session['undo'].append((session['lhs'], session['rhs']))
    if left_right == 'comb_lhs':
        lhs = together(latex2sympy(session['lhs']))
        session['lhs'] = clean_up(latex(lhs))
    elif left_right == 'comb_rhs':
        rhs = together(latex2sympy(session['rhs']))
        session['rhs'] = clean_up(latex(rhs))
    check_complete()
    return_tuple = (session['lhs'], session['rhs'])
    return jsonify(return_tuple)

@equations.route('/swap')
def swap():
    session['undo'].append((session['lhs'], session['rhs']))
    session['lhs'], session['rhs'] = session['rhs'], session['lhs']
    check_complete()
    return_tuple = (session['lhs'], session['rhs'])
    return jsonify(return_tuple)

@equations.route('/undo')
def undo():
    if len(session['undo']) > 0:
        my_equation = session['undo'].pop()
        session['lhs'], session['rhs'] = my_equation[0], my_equation[1]
    return_tuple = (session['lhs'], session['rhs'])
    return jsonify(return_tuple)

@equations.route('/hint')
def hint():
    if session.get('hints'):
        session['hints'] += 1
    else:
        session['hints'] = 1
    lhs = latex2sympy(session['lhs'])
    lhs_tree = preorder_traversal(lhs)
    hint = None
    tree = None
    if len(list(lhs_tree)) > 3:
        tree = preorder_traversal(lhs)
    else:
        rhs = latex2sympy(session['rhs'])
        rhs_tree = preorder_traversal(rhs)
        if len(list(rhs_tree)) > 3:
            tree = preorder_traversal(rhs)
    if tree:
        for node in tree:
            if isinstance(node, Mul):
                if isinstance(node.args[-1], Pow):
                    hint = 'mul'
                    break
                hint = 'div'
                break
            elif isinstance(node, Add):
                hint = '+-'
                break
    return json.dumps(hint)


@equations.route('/new_equation', methods=["GET", "POST"])
@login_required
def new_equation():
    if current_user.role != 'teacher':
        flash('You do not have permission to perform that action.')
        return redirect(url_for('users.profile'))
    form = NewEquation()
    teacher = Teacher.query.filter_by(user_id=current_user.user_id).first()
    if form.validate_on_submit():
        backslash_lhs = form.lhs.data.replace('\\', '\\\\')
        backslash_rhs = form.rhs.data.replace('\\', '\\\\')
        app.logger.info(backslash_lhs)
        app.logger.info(backslash_rhs)
        try:
            new_lhs = latex2sympy(backslash_lhs)
            new_rhs = latex2sympy(backslash_rhs)
            new_lhs += 2*x
            new_rhs += 2*x
        except:
            flash("Input not accepted")
            return render_template('new_equation.html', form=form)
        else:
            new_equation = Equation(teacher.teacher_id, backslash_lhs, backslash_rhs)
            db.session.add(new_equation)
            db.session.commit()
    
    return render_template('new_equation.html', form=form)
