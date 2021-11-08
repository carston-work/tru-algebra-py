from flask import Blueprint, render_template, session
from random import randint


main = Blueprint('main', __name__, template_folder="templates")


@main.route('/')
def home():
    demo_id = randint(1, 10)
    session.permanent = False
    return render_template('home.html', demo_id=demo_id)