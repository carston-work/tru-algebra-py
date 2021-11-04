from flask_wtf import FlaskForm
from wtforms.fields import SelectField, SubmitField, StringField
from wtforms.validators import InputRequired, DataRequired, Length

class DiffRating(FlaskForm):
    diff = SelectField("Difficulty", choices=[
        ('1', 'Very Easy'),
        ('2', 'Easy'),
        ('3', 'Average'),
        ('4', 'Difficult'),
        ('5', 'Very Difficult'),
        ], validators=[InputRequired()])
    submit = SubmitField("Save and Submit")


class NewEquation(FlaskForm):
    lhs = StringField('', validators=[
        InputRequired('Left hand side is empty'),
        DataRequired('Left hand side is empty'),
        Length(min=1, max=128, message="Left hand side must be between 1 and 128 characters.")
    ])
    rhs = StringField('', validators=[
        InputRequired('Right hand side is empty'),
        DataRequired('Right hand side is empty'),
        Length(min=1, max=128, message="Right hand side must be between 1 and 128 characters.")
    ])
    submit = SubmitField('Submit')