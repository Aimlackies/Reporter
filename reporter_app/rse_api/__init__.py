from flask import Blueprint

bp = Blueprint('rse_api', __name__)

from reporter_app.rse_api import routes
from reporter_app.rse_api import forms
