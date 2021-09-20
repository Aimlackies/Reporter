from flask import flash, request
from flask import render_template, url_for, redirect
from reporter_app.rse_api import bp
from reporter_app.models import User, Role, RealPowerReadings, RealSiteReadings
from reporter_app import db
from reporter_app.rse_api.utils import get_device_power, get_site_info
from datetime import datetime, timedelta
from flask_security import auth_required, current_user, roles_required


class Live_entry:
	date_time=""
	device_name=""
	power=""
	
	

def current_situation(query):
	'''
doesble check whether this works,
perhpas assigning is wrong???
function get_device_power contains 
return {'datetime': date_time, 'power': power}
get_site_info - return {'datetime': date_time, 'power': power, 'temperature': temperature}
    '''
	current_entries=[]
	for row in query:
		entry = Live_entry()
		entry.date_time=row.date_time
		entry.power=row.power
		entry.device_name=row.device_name
		current_entries.append(entry)
	return current_entries

@bp.route('/live_system')
@auth_required("token", "session")
@roles_required('verified')
def live_system():
	start_date = datetime.now() - timedelta(hours=6)
	query = RealPowerReadings.query.filter(RealPowerReadings.create_datetime>start_date).all()
	"try adding power for each well"
	#power=get_device_power("Llanwrtyd Wells - Wind Generator 1")
	#entries = current_situation(power)  
	powers=current_situation(query)
	#powers.append(power)
	return render_template('rse_api/live_system.html',  powers=powers)

@bp.route('/live_system/30m')
@auth_required("token", "session")
@roles_required('verified')
def live_system_30():
	start_date = datetime.now() - timedelta(minutes=30)
	query = RealPowerReadings.query.filter(RealPowerReadings.create_datetime>start_date).all()
	"try adding power for each well"
	#power=get_device_power("Llanwrtyd Wells - Wind Generator 1")
	#entries = current_situation(power)  
	powers=current_situation(query)
	#powers.append(power)
	return render_template('rse_api/live_system.html',  powers=powers)

@bp.route('/live_system/1h')
@auth_required("token", "session")
@roles_required('verified')
def live_system_1h():
	start_date = datetime.now() - timedelta(hours=1)
	query = RealPowerReadings.query.filter(RealPowerReadings.create_datetime>start_date).all()
	"try adding power for each well"
	#power=get_device_power("Llanwrtyd Wells - Wind Generator 1")
	#entries = current_situation(power)  
	powers=current_situation(query)
	#powers.append(power)
	return render_template('rse_api/live_system.html',  powers=powers)


@bp.route('/live_system/6h')
@auth_required("token", "session")
@roles_required('verified')
def live_system_6h():
	start_date = datetime.now() - timedelta(hours=6)
	query = RealPowerReadings.query.filter(RealPowerReadings.create_datetime>start_date).all()
	"try adding power for each well"
	#power=get_device_power("Llanwrtyd Wells - Wind Generator 1")
	#entries = current_situation(power)  
	powers=current_situation(query)
	#powers.append(power)
	return render_template('rse_api/live_system.html',  powers=powers)

@bp.route('/live_system/12h')
@auth_required("token", "session")
@roles_required('verified')
def live_system_12h():
	start_date = datetime.now() - timedelta(hours=12)
	query = RealPowerReadings.query.filter(RealPowerReadings.create_datetime>start_date).all()
	"try adding power for each well"
	#power=get_device_power("Llanwrtyd Wells - Wind Generator 1")
	#entries = current_situation(power)  
	powers=current_situation(query)
	#powers.append(power)
	return render_template('rse_api/live_system.html',  powers=powers)

@bp.route('/live_system/24h')
@auth_required("token", "session")
@roles_required('verified')
def live_system_24h():
	start_date = datetime.now() - timedelta(hours=24)
	query = RealPowerReadings.query.filter(RealPowerReadings.create_datetime>start_date).all()
	"try adding power for each well"
	#power=get_device_power("Llanwrtyd Wells - Wind Generator 1")
	#entries = current_situation(power)  
	powers=current_situation(query)
	#powers.append(power)
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

