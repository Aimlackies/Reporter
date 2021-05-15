from flask import flash, request
from flask import render_template, url_for, redirect
from reporter_app.users import bp
from reporter_app.models import User, Role
from reporter_app import db
from flask_security import auth_required, current_user, roles_required


@bp.route('/user/<id>')
@auth_required("token", "session")
def user(id):
	user = User.query.filter_by(id=id).first_or_404()
	# If the user accessing the page has permission render user
	if user.id == current_user.id or (current_user.has_role('admin') and current_user.has_role('verified')):  # Only user owner and admin allowed
		# Get all roles according to the user
		roles = Role.query.all()
		hasRoles = []
		otherRoles = []
		for role in roles:
			# We manage verified role seperatly
			if role.name == 'verified':
				continue
			if user.has_role(role.name):
				hasRoles.append(role)
			else:
				otherRoles.append(role)
		return render_template('users/user.html', user=user, has_roles=hasRoles, other_roles=otherRoles)
	# If the user does not have permission then redirect to dashboard
	flash('You do not have permission to do that', 'danger')
	return redirect(url_for('dashboard.dashboard'))


@bp.route('/users/')
@auth_required("token", "session")
@roles_required('verified', 'admin')
def users():
	# If the user accessing the page has permission render users
	if current_user.has_role('admin'):  # Only user owner and admin allowed
		users = User.query.all()
		return render_template('users/users.html', users=users)
	# If the user does not have permission then redirect to dashboard
	flash('You do not have permission to do that', 'danger')
	return redirect(url_for('dashboard.dashboard'))


@bp.route('/user/<id>/toggle_role/<role_name>')
@auth_required("token", "session")
def toggle_user_role(id, role_name):
	user = User.query.filter_by(id=id).first_or_404()
	# If the user accessing the route has permission render user
	# A user has to be an admin, verified and a user cannot change their own permissions
	if (current_user.id != int(id)) and current_user.has_role('admin') and current_user.has_role('verified'):
		role = Role.query.filter_by(name=role_name).first()
		if user.has_role(role_name):
			user.roles.remove(role)
			db.session.commit()
		else:
			user.roles.append(role)
			db.session.commit()
		return redirect(url_for('users.user', id=user.id))
	# If the user does not have permission then reload user template
	flash('You do not have permission to do that', 'danger')
	#return redirect(url_for('users.user', id=user.id), code=403)
	return render_template('errors/403.html'), 403
