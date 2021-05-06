from flask import Blueprint

bp = Blueprint('electricity_use', __name__)

from reporter_app.electricity_use import routes
from reporter_app.electricity_use import forms

