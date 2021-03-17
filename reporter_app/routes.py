from flask import Flask, request, Response, flash
from flask import render_template, url_for, redirect
from reporter_app import app, db

from flask_security import auth_required, hash_password, current_user


@app.route('/')
@app.route('/dashboard')
@auth_required("token", "session")
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

'''
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
'''
