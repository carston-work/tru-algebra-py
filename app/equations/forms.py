from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import SelectField, SubmitField
from wtforms.validators import InputRequired, DataRequired

class DiffRating(FlaskForm):
    diff = SelectField("Difficulty", choices=[
        ('1', 'Very Easy'),
        ('2', 'Easy'),
        ('3', 'Average'),
        ('4', 'Difficult'),
        ('5', 'Very Difficult'),
        ], validators=[InputRequired()])
    submit = SubmitField("Save and Submit")