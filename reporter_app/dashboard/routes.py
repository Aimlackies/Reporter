from flask import Flask, request, Response, flash
from flask import render_template, url_for, redirect
from reporter_app.dashboard import bp
from reporter_app import db
from reporter_app.models import User
from flask_security import auth_required, hash_password, current_user


@bp.route('/')
@bp.route('/dashboard')
@auth_required("token", "session")
def dashboard():
    return render_template('dashboard/dashboard.html', title='Dashboard')
