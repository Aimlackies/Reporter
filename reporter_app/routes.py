from flask import Flask, request, Response, flash
from flask import render_template, url_for, redirect
from reporter_app import app, db
from reporter_app.models import User
from flask_security import auth_required, hash_password, current_user


@app.route('/')
@app.route('/dashboard')
@auth_required("token", "session")
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@app.route('/profile/<id>')
@auth_required("token", "session")
def profile(id):
    user = User.query.filter_by(id=id).first_or_404()
    # If the user accessing the page is not that use then redirect to dashboard
    if user.id != current_user.id:
        flash('You do not have permission to do that', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('profile.html', user=user)
