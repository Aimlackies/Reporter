from flask import Blueprint

bp = Blueprint('co2', __name__)

from reporter_app.co2 import routes
from reporter_app.co2 import forms

