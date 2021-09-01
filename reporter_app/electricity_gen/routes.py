from flask import Flask, render_template, url_for, redirect
from reporter_app.electricity_gen import bp
from reporter_app import db
from reporter_app.models import User, ElecGen
import pandas as pd
from reporter_app.electricity_gen.utils import call_leccyfunc
from flask_security import auth_required, roles_required
from datetime import datetime, timedelta


@bp.route('/electricity_gen')
@auth_required("token", "session")
@roles_required('verified')
def electricity_gen():
    start_date = datetime.now() - timedelta(hours=24)
    e_gen_entries = ElecGen.query.filter(ElecGen.date_time>start_date).all()
    return render_template('electricity_gen/electricity_gen.html',
                           e_gen_entries=e_gen_entries)


@bp.route('/electricity_gen/48_hours')
@auth_required("token", "session")
@roles_required('verified')
def e_use_48h():
    start_date = datetime.now() - timedelta(hours=48)
    e_gen_entries = ElecGen.query.filter(ElecGen.date_time>start_date).all()
    return render_template('electricity_gen/electricity_gen.html',
                           e_gen_entries=e_gen_entries)


@bp.route('/electricity_gen/7_days')
@auth_required("token", "session")
@roles_required('verified')
def e_use_7d():
    start_date = datetime.now() - timedelta(days=7)
    e_gen_entries = ElecGen.query.filter(ElecGen.date_time>start_date).all()
    return render_template('electricity_gen/electricity_gen.html',
                           e_gen_entries=e_gen_entries)


@bp.route('/electricity_gen/28_days')
@auth_required("token", "session")
@roles_required('verified')
def e_use_28d():
    start_date = datetime.now() - timedelta(days=28)
    e_gen_entries = ElecGen.query.filter(ElecGen.date_time>start_date).all()
    return render_template('electricity_gen/electricity_gen.html',
                           e_gen_entries=e_gen_entries)


@bp.route('/electricity_gen/all')
@auth_required("token", "session")
@roles_required('verified')
def e_use_all():
    e_gen_entries = ElecGen.query.all()
    return render_template('electricity_gen/electricity_gen.html',
                           e_gen_entries=e_gen_entries)
