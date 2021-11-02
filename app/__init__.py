from flask import Flask
from app.extensions import *
import os


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get('RECAPTCHA_PRIVATE_KEY')

    init_extensions(app)

    # import and add Blueprints here
    from app.main.views import home, main
    from app.auth.views import auth
    from app.users.views import users
    from app.classes.views import classes
    from app.assignments.views import assignments
    from app.equations.views import equations
    app.add_url_rule('/', view_func=home)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(classes, url_prefix='/classes')
    app.register_blueprint(assignments, url_prefix='/assignments')
    app.register_blueprint(equations, url_prefix='/equations')


    return app