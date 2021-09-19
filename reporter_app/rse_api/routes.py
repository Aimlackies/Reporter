from flask import flash, request
from flask import render_template, url_for, redirect
from reporter_app.rse_api import bp
from reporter_app.models import User, Role, RealPowerReadings, RealSiteReadings
from reporter_app import db
from reporter_app.rse_api.utils import get_device_power, get_site_info
from datetime import datetime, timedelta
from flask_security import auth_required, current_user, roles_required

"to do: add the remaining wells, remove the graph"
# class Live_entry:
# 	datetime=""
# 	temperature=""
# 	power=""
	

# def current_situation(query):
# 	'''
# doesble check whether this works,
# perhpas assigning is wrong???
# function get_device_power contains 
# return {'datetime': date_time, 'power': power}
# get_site_info - return {'datetime': date_time, 'power': power, 'temperature': temperature}
#     '''
# 	current_entries=[]
# 	for row in query:
# 		entry = Live_entry()
# 		entry.datetime=row["date_time"]
# 		entry.power=row["power"]
# 		entry.temperature=row["temperature"]
# 		current_entries.append(entry)
# 	return current_entries



@bp.route('/live_system/Llanwrtyd Wells - Wind Generator 1')
@auth_required("token", "session")
@roles_required('verified')

def live_system():
	powers=[]
	# start_date = datetime.now() - timedelta(hours=24)
	# power = RealSiteReadings.query.filter(RealSiteReadings.date_time>start_date).all()
	"try adding power for each well"
	power=get_device_power("Llanwrtyd Wells - Wind Generator 1")
	#entries = current_situation(power)  
	powers.append(power)
	return render_template('rse_api/live_system.html',  powers=powers)

# @bp.route('/live_system')
# @auth_required("token", "session")
# @roles_required('verified')
# def all_dat():
# 	data=[]
# 	dat=get_site_info()
# 	print(dat)
# 	print("zrobione")
# 	data.append(dat)
# 	return render_template('rse_api/live_system.html',  data=data)




# def live_system():
# 	powers=[]
# 	# this gives you a dictionary
# 	power = get_site_info() 
# 	powers.append(power)
# 	return render_template('rse_api/live_system.html',  powers=powers)


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

