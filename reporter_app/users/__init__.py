from flask import Blueprint

bp = Blueprint('users', __name__)

from reporter_app.users import routes
from reporter_app.users import forms
