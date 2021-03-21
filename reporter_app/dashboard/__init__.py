from flask import Blueprint

bp = Blueprint('dashboard', __name__)

from reporter_app.dashboard import routes
from reporter_app.dashboard import forms
