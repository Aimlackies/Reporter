from flask import Flask, render_template, url_for, redirect
from reporter_app.net_power import bp
from reporter_app import db
from reporter_app.models import User, ElecUse, ElecGen
import pandas as pd
from reporter_app.electricity_use.utils import call_leccyfunc
from flask_security import auth_required, roles_required
from datetime import datetime, timedelta


@bp.route('/net_power')
@auth_required("token", "session")
@roles_required('verified')
def net_power():
    start_date = datetime.now() - timedelta(hours=24)
    e_use_entries = ElecUse.query.filter(ElecUse.date_time>start_date).all()
    e_gen_entries = ElecGen.query.filter(ElecGen.date_time>start_date).all()
    return render_template('net_power/net_power.html',
                           e_use_entries=e_use_entries, e_gen_entries=e_gen_entries)


@bp.route('/net_power/48_hours')
@auth_required("token", "session")
@roles_required('verified')
def np_48h():
    start_date = datetime.now() - timedelta(hours=48)
    e_use_entries = ElecUse.query.filter(ElecUse.date_time>start_date).all()
    return render_template('net_power/net_power.html',
                           e_use_entries=e_use_entries)


@bp.route('/net_power/7_days')
@auth_required("token", "session")
@roles_required('verified')
def np_7d():
    start_date = datetime.now() - timedelta(days=7)
    e_use_entries = ElecUse.query.filter(ElecUse.date_time>start_date).all()
    return render_template('net_power/net_power.html',
                           e_use_entries=e_use_entries)


@bp.route('/net_power/28_days')
@auth_required("token", "session")
@roles_required('verified')
def np_28d():
    start_date = datetime.now() - timedelta(days=28)
    e_use_entries = ElecUse.query.filter(ElecUse.date_time>start_date).all()
    return render_template('net_power/net_power.html',
                           e_use_entries=e_use_entries)
