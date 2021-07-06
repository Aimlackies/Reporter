from flask import Flask, render_template, url_for, redirect
from reporter_app.electricity_use import bp
from reporter_app import db
from reporter_app.models import User, eUse
import pandas as pd
from reporter_app.electricity_use.utils import call_leccyfunc
from flask_security import auth_required, roles_required
from datetime import datetime, timedelta


@bp.route('/electricity_use')
@auth_required("token", "session")
@roles_required('verified')
def electricity_use():
    start_date = datetime.now() - timedelta(hours=24)
    e_use_entries = eUse.query.filter(eUse.date_time>start_date).all()
    return render_template('electricity_use/electricity_use.html',
                           e_use_entries=e_use_entries)


@bp.route('/electricity_use/48_hours')
@auth_required("token", "session")
@roles_required('verified')
def e_use_48h():
    start_date = datetime.now() - timedelta(hours=48)
    e_use_entries = eUse.query.filter(eUse.date_time>start_date).all()
    return render_template('electricity_use/electricity_use.html',
                           e_use_entries=e_use_entries)


@bp.route('/electricity_use/7_days')
@auth_required("token", "session")
@roles_required('verified')
def e_use_7d():
    start_date = datetime.now() - timedelta(days=7)
    e_use_entries = eUse.query.filter(eUse.date_time>start_date).all()
    return render_template('electricity_use/electricity_use.html',
                           e_use_entries=e_use_entries)


@bp.route('/electricity_use/28_days')
@auth_required("token", "session")
@roles_required('verified')
def e_use_28d():
    start_date = datetime.now() - timedelta(days=28)
    e_use_entries = eUse.query.filter(eUse.date_time>start_date).all()
    return render_template('electricity_use/electricity_use.html',
                           e_use_entries=e_use_entries)


@bp.route('/electricity_use/all')
@auth_required("token", "session")
@roles_required('verified')
def e_use_all():
    e_use_entries = eUse.query.all()
    return render_template('electricity_use/electricity_use.html',
                           e_use_entries=e_use_entries)


