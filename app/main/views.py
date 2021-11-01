from flask import Blueprint, render_template
from random import randint


main = Blueprint('main', __name__, template_folder="templates")


@main.route('/', methods=['GET'])
def home():
    demo_id = randint(1, 10)
    return render_template('home.html', demo_id=demo_id)