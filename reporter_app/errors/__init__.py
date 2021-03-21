from flask import Blueprint

bp = Blueprint('errors', __name__)

from reporter_app.errors import routes
