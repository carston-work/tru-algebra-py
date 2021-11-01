from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length


class RegistrationForm(FlaskForm):
    username = StringField("Username: ", validators=[
        InputRequired("You must supply a username"),
        DataRequired("Your username cannot be blank")
    ])
    first = StringField("First Name: ", validators=[
        InputRequired(),
        DataRequired()
    ])
    last = StringField("Last Name: ", validators=[
        InputRequired(),
        DataRequired()
    ])
    password = PasswordField("Password", validators=[
        InputRequired("You need a password!"),
        DataRequired("Your password cannot be a bunch of blank characters."),
        Length(min=8, max=20, message="Password must be between 8 and 20 characters in length."),
        EqualTo("password_confirm", message="Passwords do not match")                      
    ])
    password_confirm = PasswordField("Confirm Password: ", validators=[
        InputRequired("Please confirm your password"),
        DataRequired("Please confirm your password"),
        Length(min=8, max=20, message="Password must be between 8 and 20 characters in length."),                      
    ])
    role = RadioField("I am a: ", choices=[('2', 'Student'), ('1', 'Teacher')], validators=[InputRequired('You must select a role.')])
    title = StringField("Preferred Title: ", validators=[Length(max=10, message="Title must be 10 characters or less")])
    recaptcha = RecaptchaField()
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[
        InputRequired("You must supply a username"),
        DataRequired("Your username cannot be blank")
    ])
    password = PasswordField("Password", validators=[
        InputRequired("You must type your password to log in!"),
        DataRequired("You must type your password to log in!")                 
    ])
    remember_me = BooleanField("Remember Me: ")
    submit = SubmitField("Login")
    
