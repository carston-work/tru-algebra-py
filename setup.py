from app import db, create_app
import os


app = create_app()
app.app_context().push()

def create_equations():
    from app.models import Equation

    equations = [
        (1, '2\\left(-7\\left(x-4\\right)-4\\right)', '-4\\left(x-4\\right)-14'),
        (1, '\\frac{x-1}{-1}-10', '-3\\left(x-7\\right)-8'),
        (1, '\\frac{5\\left(x+5\\right)}{6}', '\\frac{-4\\left(\\frac{x}{-4}-2\\right)+3}{3}'),
        (1, '\\frac{3\\left(x+1\\right)}{5}', '-1\\left(\\frac{\\frac{x}{-4}-17}{5}+4\\right)'),
        (1, '\\frac{x+7}{56}+4', '\\frac{-115x}{28}'),
        (1, '\\frac{\\frac{x}{2}+4}{-8}', '\\frac{x+15}{-128}'),
        (1, '5\\left(x-4\\right)-10', '\\frac{8x+25}{-11}-22'),
        (1, '\\frac{7\\left(x-5\\right)}{5}', '2\\left(x+5\\right)-17'),
        (1, '\\frac{-1\\left(x-6\\right)}{896}', '\\frac{x+3}{3}-3'),
        (1, '-15\\left(x+18\\right)+10', '100x-30'),
    ]

    for equation in equations:
        eq = Equation(equation[0], equation[1], equation[2])
        db.session.add(eq)


def create_perfs():
    from app.models import Performance

    perfs = [
        (1, 1, 1, 2),
        (1, 1, 2, 5),
        (1, 2, 1, 3),
        (1, 2, 2, 3),
        (1, 3, 1, 4),
        (1, 3, 2, 1),
        (1, 4, 1, 5),
        (1, 4, 2, 3),
        (1, 5, 1, 2),
        (1, 5, 2, 4),
        (1, 6, 1, 3),
        (1, 6, 2, 3),
        (1, 7, 1, 2),
        (1, 7, 2, 5),
        (1, 8, 1, 1),
        (1, 8, 2, 5),
        (1, 9, 1, 5),
        (1, 9, 2, 5),
        (1, 10, 1, 2),
        (1, 10, 2, 3),
    ]

    for perf in perfs:
        p = Performance(perf[0], perf[1], attempt=perf[2], diff_rating=perf[3])
        db.session.add(p)





def reset():
    from app.models import Teacher, Student, Class
    db.drop_all()
    db.create_all()
    owner = Teacher('cheat-commando', 'Cheat', 'Commando', os.environ.get('OWNER_PASSWORD'), 'Mr.')
    owner_class = Class(1, 'Foundations 6')
    student = Student('code-monkey', 'Code', 'Monkey', os.environ.get('STUDENT_PASSWORD'), 1)
    db.session.add(owner)
    db.session.add(owner_class)
    db.session.add(student)
    create_equations()
    create_perfs()
    db.session.commit()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))