from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_security import RegisterForm


class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('First Name', [DataRequired()])
    surname = StringField('Surname', [DataRequired()])
