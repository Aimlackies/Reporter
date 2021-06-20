from flask import Flask, render_template, url_for, redirect
from reporter_app.co2 import bp
from reporter_app import db
from reporter_app.models import User
from reporter_app.models import Co2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_security import auth_required, roles_required


@bp.route('/co2')
@auth_required("token", "session")
@roles_required('verified')
def co2():
    co2_entries = Co2.query.all()
    return render_template('co2/co2.html', co2_entries=co2_entries)
