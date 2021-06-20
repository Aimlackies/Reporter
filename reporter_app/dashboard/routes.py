from flask import Flask, request, Response, flash
from flask import render_template, url_for, redirect
from reporter_app.dashboard import bp
from reporter_app import db
from reporter_app.models import User
from flask_security import auth_required, hash_password, current_user, roles_required

# for graphs
import pandas as pd
import json


@bp.route('/')
@bp.route('/dashboard')
@auth_required("token", "session")
@roles_required('verified')
def dashboard():
	return render_template('dashboard/dashboard.html', title='Dashboard')

@bp.route('/new_user')
@auth_required("token", "session")
def new_user():
	return render_template('dashboard/new_user.html', title='Congratulations for signing up!')
