from flask import Blueprint

bp= Blueprint('trading',__name__)

from reporter_app.trading import routes

from reporter_app.trading import forms