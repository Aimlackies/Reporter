#all the blueprints
from flask import Blueprint

bp = Blueprint('reports', __name__)

from reporter_app.rse_api import routes
from reporter_app.rse_api import forms



