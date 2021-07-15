from flask import Blueprint

bp = Blueprint('electricity_gen', __name__)

from reporter_app.electricity_gen import routes
from reporter_app.electricity_gen import forms

