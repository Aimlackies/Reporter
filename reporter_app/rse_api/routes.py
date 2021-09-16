from flask import flash, request
from flask import render_template, url_for, redirect
from reporter_app.rse_api import bp
from reporter_app.models import User, Role, RealPowerReadings
from reporter_app import db
from flask_security import auth_required, current_user, roles_required


@bp.route('/live_system')
@auth_required("token", "session")
@roles_required('verified')
def live_system():
	return render_template('rse_api/live_system.html', title='Live system')
