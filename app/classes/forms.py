from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import InputRequired, DataRequired
class ClassForm(FlaskForm):
    class_name = StringField("Class Name: ", validators=[
        InputRequired("Your class needs a name"),
        DataRequired("Your class needs a name")
    ])
    submit = SubmitField("Create Class")


class ClassSearchForm(FlaskForm):
    teacher_last_name = StringField("Teacher's Last Name: ", validators=[
        InputRequired("Enter a search term"),
        DataRequired("Enter a search term")
    ])
    teacher_first_name = StringField("Teacher's First Name: ")
    submit = SubmitField("Search")

