from flask import Flask, render_template, url_for, redirect
from reporter_app.co2 import bp
from reporter_app import db
from reporter_app.models import User
from reporter_app.models import Co2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_security import auth_required, roles_required
from sqlalchemy import func
from datetime import datetime, timedelta


@bp.route('/co2')
@auth_required("token", "session")
@roles_required('verified')
def co2():
    start_date = datetime.now() - timedelta(hours=24) #Get the start date
    co2_entries = Co2.query.filter(Co2.date_time>start_date).all() #filter when the date_time is greater than start
    return render_template('co2/co2.html', co2_entries=co2_entries) # render template according to the entries

@bp.route('/co2/48_hours')
@auth_required("token", "session")
@roles_required('verified')
def co2_48hours(): #if someone clicks 48 hour view do this
    start_date = datetime.now() - timedelta(hours=48) 
    co2_entries = Co2.query.filter(Co2.date_time>start_date).all() # the co2 database has everything you just need to filter
    return render_template('co2/co2.html', co2_entries=co2_entries)

@bp.route('/co2/7_days')
@auth_required("token", "session")
@roles_required('verified')
def co2_7days():
    start_date = datetime.now() - timedelta(days=7)
    co2_entries = Co2.query.filter(Co2.date_time>start_date).all()
    return render_template('co2/co2.html', co2_entries=co2_entries)

@bp.route('/co2/28_days')
@auth_required("token", "session")
@roles_required('verified')
def co2_28days():
    start_date = datetime.now() - timedelta(days=28)
    co2_entries = Co2.query.filter(Co2.date_time>start_date).all()
    return render_template('co2/co2.html', co2_entries=co2_entries)

@bp.route('/co2/all')
@auth_required("token", "session")
@roles_required('verified')
def co2_all():
    co2_entries = Co2.query.all() # The real question is where has this CO2 been defined
    return render_template('co2/co2.html', co2_entries=co2_entries)