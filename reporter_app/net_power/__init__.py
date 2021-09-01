from flask import Blueprint

bp = Blueprint('net_power', __name__)

from reporter_app.net_power import routes
from reporter_app.net_power import forms

