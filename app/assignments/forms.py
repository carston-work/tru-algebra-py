from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, DataRequired


class AssignmentFilter(FlaskForm):
    lower_bound = IntegerField("minimum difficulty: ")
    upper_bound = IntegerField("maximum difficulty: ")