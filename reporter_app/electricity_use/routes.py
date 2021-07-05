from flask import Flask, render_template, url_for, redirect
from reporter_app.electricity_use import bp
from reporter_app import db
from reporter_app.models import User
import pandas as pd
from reporter_app.electricity_use.utils import call_leccyfunc
from flask_security import auth_required, roles_required


@bp.route('/electricity_use')
@auth_required("token", "session")
@roles_required('verified')
def electricity_use():
    df = call_leccyfunc()
    return render_template('electricity_use/electricity_use.html',
                           column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)
