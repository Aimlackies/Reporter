from wtforms import StringField
from wtforms.validators import DataRequired
from flask_security import RegisterForm, LoginForm
from flask_security.utils import find_user, get_message, hash_password
from flask_security.confirmable import requires_confirmation
from flask import flash
from werkzeug.local import LocalProxy
from reporter_app import app as current_app


class ExtendedRegisterForm(RegisterForm):
    """
    Add first_name and surname to register form from Flask-security-too
    """
    first_name = StringField('First Name', [DataRequired()])
    surname = StringField('Surname', [DataRequired()])


# Add
class ExtendedLoginForm(LoginForm):
    """
    Extended login form to remove default error messages and add flash
    messages
    """

    def validate(self):

        super(ExtendedLoginForm, self).validate()

        _security = LocalProxy(lambda: current_app.extensions["security"])

        self.user = find_user(self.email.data)

        if self.user is None:
            self.email.errors.append(get_message("USER_DOES_NOT_EXIST")[0])
            flash(get_message("USER_DOES_NOT_EXIST")[0], get_message("USER_DOES_NOT_EXIST")[1])
            # Reduce timing variation between existing and non-existing users
            hash_password(self.password.data)
            return False
        if not self.user.password:
            flash(get_message("PASSWORD_NOT_SET")[0], get_message("PASSWORD_NOT_SET")[1])
            # Reduce timing variation between existing and non-existing users
            hash_password(self.password.data)
            return False
        self.password.data = _security._password_util.normalize(self.password.data)
        if not self.user.verify_and_update_password(self.password.data):
            self.password.errors.append(get_message("INVALID_PASSWORD")[0])
            flash(get_message("INVALID_PASSWORD")[0], get_message("INVALID_PASSWORD")[1])
            return False
        self.requires_confirmation = requires_confirmation(self.user)
        if self.requires_confirmation:
            flash(get_message("CONFIRMATION_REQUIRED")[0], get_message("CONFIRMATION_REQUIRED")[1])
            return False
        if not self.user.is_active:
            flash(get_message("DISABLED_ACCOUNT")[0], get_message("DISABLED_ACCOUNT")[1])
            return False
        return True
