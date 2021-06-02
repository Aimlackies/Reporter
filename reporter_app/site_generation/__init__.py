from flask import Blueprint

bp = Blueprint('site_generation', __name__)

from reporter_app.site_generation import routes
from reporter_app.site_generation import forms