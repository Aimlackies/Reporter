from flask import flash
from flask import render_template, url_for, redirect
from reporter_app.users import bp
from reporter_app.models import User
from flask_security import auth_required, current_user, roles_required


@bp.route('/user/<id>')
@auth_required("token", "session")
def user(id):
	user = User.query.filter_by(id=id).first_or_404()
	# If the user accessing the page has permission render user
	if user.id == current_user.id or current_user.has_role('admin'):  # Only user owner and admin allowed
		return render_template('users/user.html', user=user)
	# If the user does not have permission then redirect to dashboard
	flash('You do not have permission to do that', 'danger')
	return redirect(url_for('dashboard.dashboard'))


@bp.route('/users/')
@auth_required("token", "session")
@roles_required('admin')
def users():
	# If the user accessing the page has permission render users
	if current_user.has_role('admin'):  # Only user owner and admin allowed
		users = User.query.all()
		return render_template('users/users.html', users=users)
	# If the user does not have permission then redirect to dashboard
	flash('You do not have permission to do that', 'danger')
	return redirect(url_for('dashboard.dashboard'))
