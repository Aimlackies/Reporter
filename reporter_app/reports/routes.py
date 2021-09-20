from flask import flash, request
from flask import render_template, url_for, redirect
from reporter_app.reports import bp
#and other data I need for reports
from reporter_app.models import User, Role, RealPowerReadings, RealSiteReadings, Co2, ElecGen, ElecUse
from reporter_app import db
from reporter_app.reports.utils import get_device_power, get_site_info
from datetime import datetime, timedelta
from flask_security import auth_required, current_user, roles_required


"""Revenue gained from sales
Carbon dioxide emission savings
Cost savings compared to buying 
The cost of imported electricity 
The accuracy of our prediction of energy usage and production"""

@bp.route('/reports')
@auth_required("token", "session")
@roles_required('verified')
def reports():
	start_date = datetime.now() - timedelta(hours=6)
	query = RealPowerReadings.query.filter(RealPowerReadings.create_datetime>start_date).all()
	"try adding power for each well"
	#power=get_device_power("Llanwrtyd Wells - Wind Generator 1")
	#entries = current_situation(power)  
	powers=current_situation(query)
	#powers.append(power)
	return render_template('rse_api/live_system.html',  powers=powers)
