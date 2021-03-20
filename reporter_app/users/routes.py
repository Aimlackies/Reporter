from flask import Flask, request, Response, flash
from flask import render_template, url_for, redirect
from reporter_app.users import bp
from reporter_app import db
from reporter_app.models import User
from flask_security import auth_required, hash_password, current_user

@bp.route('/user/<id>')
@auth_required("token", "session")
def user(id):
    user = User.query.filter_by(id=id).first_or_404()
    # If the user accessing the page is not that use then redirect to dashboard
    if user.id != current_user.id:
        flash('You do not have permission to do that', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('users/user.html', user=user)
