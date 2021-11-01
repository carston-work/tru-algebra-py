from flask import Flask
from app.extensions import *
from app.secrets import secret_key, pgusername, pgpass, recap_public, recap_private
from boto.s3.connection import S3Connection
import os


def create_app():
    app = Flask(__name__)
    s3 = S3Connection(os.environ[''], os.environ[''])
    app.config["SECRET_KEY"] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{pgusername}:{pgpass}@https://tru-algebra-py.herokuapp.com/:5432/tru-algebra-py'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    

    app.config["RECAPTCHA_PUBLIC_KEY"] = recap_public
    app.config["RECAPTCHA_PRIVATE_KEY"] = recap_private

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