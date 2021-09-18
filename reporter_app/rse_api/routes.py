from flask import flash, request
from flask import render_template, url_for, redirect
from reporter_app.rse_api import bp
from reporter_app.models import User, Role, RealPowerReadings, RealSiteReadings
from reporter_app import db
from datetime import datetime, timedelta
from flask_security import auth_required, current_user, roles_required


class Live_entry:
	date_time=""
	temperature=""
	power=""
	create_datetime=""

def current_situation(query):
	'''
  compare with Paul's stuff
  utils, models, cli.py
    '''
	current_entries=[]
	for row in query:
		entry = Live_entry()
		entry.date_time=row.date_time
		entry.power=row.power
		entry.temperature=row.temperature 
		#not all co2 records have corrisponding elec usege records.  The try/except statement prevents errors when this happens
		current_entries.append(entry)
	return current_entries


@bp.route('/live_system')
@auth_required("token", "session")
@roles_required('verified')
def live_system():
	powers=[]
	start_date = datetime.now() - timedelta(hours=24)
	power = RealSiteReadings.query.filter(RealSiteReadings.date_time>start_date).all()
	entries = current_situation(power)  
	powers.append(entries)
	return render_template('rse_api/live_system.html',  powers=powers)

# @bp.route('/co2')
# @auth_required("token", "session")
# @roles_required('verified')
# def co2():
#     start_date = datetime.now() - timedelta(hours=24) 			#calc the start and end times for the database query
#     query = Co2.query.filter(Co2.date_time>start_date).all() 	#query the database for records within the above period
#     co2_entries = calc_savings(query)    						#calculate the co2 savings
# #     return render_template('co2/co2.html', co2_entries=co2_entries)

# class RealSiteReadings(db.Model):
# 	__tablename__ = 'real_site_readings'
# 	date_time = Column(DateTime(), primary_key=True)
# 	temperature = Column(db.Float)
# 	power = Column(db.Float)
# 	create_datetime = Column(DateTime(), nullable=False, server_default=func.now())
# 	update_datetime = Column(
# 		DateTime(),
# 		nullable=False,
# 		server_default=func.now(),
# 		onupdate=datetime.datetime.utcnow,
# 	)
class Live_entry:
	date_time=""
	temperature=""
	power=""
	create_datetime=""

	
