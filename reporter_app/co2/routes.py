from flask import Flask, render_template, url_for, redirect
from reporter_app.co2 import bp
from reporter_app import db
from reporter_app.models import User, Co2, ElecUse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_security import auth_required, roles_required
from sqlalchemy import func
from datetime import datetime, timedelta
import sys

class Co2_entry:
	date_time=""
	co2=""
	electricity_use=""
	co2_saved=""

	
def calc_savings(query):
	'''
    Calculates the amount of CO2 emissions saved from the onsite renewables over the grid for each database row

    Parameters
    ----------
    list of co2 objects
        The result of the route query as a list of CO2 object


    Returns
    -------
    list of co2entry object
        A new list of Co2_Entry objects. These are different from the list of co2 objects passed as they contain an extra field co2_saved (in kg)
    '''
	co2_entries=[]
	for row in query:
		entry = Co2_entry()
		entry.date_time=row.date_time
		entry.co2=row.co2
		#not all co2 records have corrisponding elec usege records.  The try/except statement prevents errors when this happens
		try:
			entry.electricity_use=row.usage.electricity_use
			entry.co2_saved=(row.co2*row.usage.electricity_use)/1000
		except Exception:
			pass
		co2_entries.append(entry)
	return co2_entries

@bp.route('/co2')
@auth_required("token", "session")
@roles_required('verified')
def co2():
    start_date = datetime.now() - timedelta(hours=24) 			#calc the start and end times for the database query
    query = Co2.query.filter(Co2.date_time>start_date).all() 	#query the database for records within the above period
    co2_entries = calc_savings(query)    						#calculate the co2 savings
    return render_template('co2/co2.html', co2_entries=co2_entries)

@bp.route('/co2/48_hours')
@auth_required("token", "session")
@roles_required('verified')
def co2_48hours():
    start_date = datetime.now() - timedelta(hours=48)
    query = Co2.query.filter(Co2.date_time>start_date).all()
    co2_entries = calc_savings(query)
    return render_template('co2/co2.html', co2_entries=co2_entries)

@bp.route('/co2/7_days')
@auth_required("token", "session")
@roles_required('verified')
def co2_7days():
    start_date = datetime.now() - timedelta(days=7)
    query = Co2.query.filter(Co2.date_time>start_date).all()
    co2_entries = calc_savings(query)
    return render_template('co2/co2.html', co2_entries=co2_entries)

@bp.route('/co2/28_days')
@auth_required("token", "session")
@roles_required('verified')
def co2_28days():
    start_date = datetime.now() - timedelta(days=28)
    query = Co2.query.filter(Co2.date_time>start_date).all()
    co2_entries = calc_savings(query)
    return render_template('co2/co2.html', co2_entries=co2_entries)

@bp.route('/co2/all')
@auth_required("token", "session")
@roles_required('verified')
def co2_all():
    query = Co2.query.all()
    co2_entries = calc_savings(query)
    return render_template('co2/co2.html', co2_entries=co2_entries)