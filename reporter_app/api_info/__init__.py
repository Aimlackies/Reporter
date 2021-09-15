from flask import Blueprint

bp = Blueprint('data', __name__)

from reporter_app.api_info import routes
from reporter_app.api_info import forms
