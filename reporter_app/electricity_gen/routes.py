from flask import Flask, render_template, url_for, redirect
from reporter_app.electricity_gen import bp
from reporter_app import db
from reporter_app.models import User, ElecGen
import pandas as pd
from reporter_app.electricity_gen.utils import call_leccyfunc, get_real_power_readings_for_times
from flask_security import auth_required, roles_required
from datetime import datetime, timedelta


@bp.route('/electricity_gen')
@auth_required("token", "session")
@roles_required('verified')
def electricity_gen():
    start_date = datetime.now() - timedelta(hours=24)
    e_gen_entries = ElecGen.query.filter(ElecGen.date_time>start_date).all()

    labels = [row.date_time for row in e_gen_entries]
    wind_e_gen_data = [row.wind_gen for row in e_gen_entries]
    solar_e_gen_data = [row.solar_gen for row in e_gen_entries]

    real_wind_e_gen, real_solar_e_gen = get_real_power_readings_for_times(labels)
    return render_template('electricity_gen/electricity_gen.html',
                           data_labels=labels,
                           wind_e_gen_data=wind_e_gen_data,
                           solar_e_gen_data=solar_e_gen_data,
                           real_wind_e_gen_data=real_wind_e_gen,
                           real_solar_e_gen_data=real_solar_e_gen)


@bp.route('/electricity_gen/48_hours')
@auth_required("token", "session")
@roles_required('verified')
def e_use_48h():
    start_date = datetime.now() - timedelta(hours=48)
    e_gen_entries = ElecGen.query.filter(ElecGen.date_time>start_date).all()

    labels = [row.date_time for row in e_gen_entries]
    wind_e_gen_data = [row.wind_gen for row in e_gen_entries]
    solar_e_gen_data = [row.solar_gen for row in e_gen_entries]

    real_wind_e_gen, real_solar_e_gen = get_real_power_readings_for_times(labels)
    return render_template('electricity_gen/electricity_gen.html',
                           data_labels=labels,
                           wind_e_gen_data=wind_e_gen_data,
                           solar_e_gen_data=solar_e_gen_data,
                           real_wind_e_gen_data=real_wind_e_gen,
                           real_solar_e_gen_data=real_solar_e_gen)


@bp.route('/electricity_gen/7_days')
@auth_required("token", "session")
@roles_required('verified')
def e_use_7d():
    start_date = datetime.now() - timedelta(days=7)
    e_gen_entries = ElecGen.query.filter(ElecGen.date_time>start_date).all()

    labels = [row.date_time for row in e_gen_entries]
    wind_e_gen_data = [row.wind_gen for row in e_gen_entries]
    solar_e_gen_data = [row.solar_gen for row in e_gen_entries]

    real_wind_e_gen, real_solar_e_gen = get_real_power_readings_for_times(labels)
    return render_template('electricity_gen/electricity_gen.html',
                           data_labels=labels,
                           wind_e_gen_data=wind_e_gen_data,
                           solar_e_gen_data=solar_e_gen_data,
                           real_wind_e_gen_data=real_wind_e_gen,
                           real_solar_e_gen_data=real_solar_e_gen)


@bp.route('/electricity_gen/28_days')
@auth_required("token", "session")
@roles_required('verified')
def e_use_28d():
    start_date = datetime.now() - timedelta(days=28)
    e_gen_entries = ElecGen.query.filter(ElecGen.date_time>start_date).all()

    labels = [row.date_time for row in e_gen_entries]
    wind_e_gen_data = [row.wind_gen for row in e_gen_entries]
    solar_e_gen_data = [row.solar_gen for row in e_gen_entries]

    real_wind_e_gen, real_solar_e_gen = get_real_power_readings_for_times(labels)
    return render_template('electricity_gen/electricity_gen.html',
                           data_labels=labels,
                           wind_e_gen_data=wind_e_gen_data,
                           solar_e_gen_data=solar_e_gen_data,
                           real_wind_e_gen_data=real_wind_e_gen,
                           real_solar_e_gen_data=real_solar_e_gen)


@bp.route('/electricity_gen/all')
@auth_required("token", "session")
@roles_required('verified')
def e_use_all():
    e_gen_entries = ElecGen.query.all()

    labels = [row.date_time for row in e_gen_entries]
    wind_e_gen_data = [row.wind_gen for row in e_gen_entries]
    solar_e_gen_data = [row.solar_gen for row in e_gen_entries]

    real_wind_e_gen, real_solar_e_gen = get_real_power_readings_for_times(labels)

    return render_template('electricity_gen/electricity_gen.html',
                           data_labels=labels,
                           wind_e_gen_data=wind_e_gen_data,
                           solar_e_gen_data=solar_e_gen_data,
                           real_wind_e_gen_data=real_wind_e_gen,
                           real_solar_e_gen_data=real_solar_e_gen)
