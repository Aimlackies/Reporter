from conftest import app_client, STANDARD_USER, ADMIN_USER, db
from utils import create_user, login
from reporter_app.models import Role, User
import pytest
from flask_security import current_user
from sqlalchemy.sql import func
import secrets
from flask import request


STANDARD_USER_2 = {
	'username': 'standard2',
	'first_name': 'standard2',
	'surname': 'standard2',
	'email': 'standard2@aimlackies.com',
	'password': 'password',
	'confirmed_at': func.now(),
	'fs_uniquifier': secrets.token_urlsafe(64),
	'active': True
}

ADMIN_USER_2 = {
	'username': 'admin2',
	'first_name': 'admin2',
	'surname': 'admin2',
	'email': 'admin2@aimlackies.com',
	'password': 'password',
	'confirmed_at': func.now(),
	'fs_uniquifier': secrets.token_urlsafe(64),
	'active': True
}


# Users page

@pytest.mark.parametrize("user_params, expect", [
	([ADMIN_USER, 'admin', True], [200]),
	([ADMIN_USER, 'admin', False], [403]),
	([STANDARD_USER, 'standard', True], [403]),
	([STANDARD_USER, 'standard', False], [403]),
	(None, [302]),
])
def test_users_page(db, app_client, user_params, expect):
	"""
	GIVEN a Flask application configured for testing and zero or one user parameters
	WHEN the '/users/' page is requested (GET)
	THEN make sure only verified admins can access it and correct status code for all access attempts

	parmas:
	user_params: [dict of user parameters, string user role, bool verifed]
	expect: [int expected response code]
	"""
	if user_params != None:
		create_user(db, user_params[0], user_params[1], verified=user_params[2])
		login(app_client, user_params[0]['email'], user_params[0]['password'])

	response = app_client.get('/users/', follow_redirects=False)
	assert response.status_code == expect[0]
	# If user logged in then make sure their parameeters are as expected
	if current_user.is_authenticated:
		assert current_user.has_role(user_params[1]) == True
		if user_params[2]:
			assert current_user.has_role('verified') == True
		else:
			assert current_user.has_role('verified') == False
	# Else make sure no user was provided and meant to be logged in
	else:
		assert user_params == None


# User profile page

@pytest.mark.parametrize("user_params, loggin_user, expect", [
	([ADMIN_USER, 'admin', True], True, [200]),
	([ADMIN_USER, 'admin', False], True, [200]),
	([ADMIN_USER, 'admin', True], False, [302]),  # redirect to login
	([STANDARD_USER, 'standard', True], True, [200]),
	([STANDARD_USER, 'standard', False], True, [200]),
	([STANDARD_USER, 'standard', True], False, [302]),  # redirect to login
])
def test_user_profile_single_user(db, app_client, user_params, loggin_user, expect):
	"""
	GIVEN a Flask application configured for testing and user parameters
	WHEN the '/user/<id>' page is requested (GET)
	THEN check that the response is 200 if the user is accessing their own page and 302 if a non logged in user is accessing the page

	parmas:
	user_params: [dict of user parameters, string user role, bool verifed]
	loggin_user: bool specifying if the user is logged in
	expect: [int expected response code]
	"""
	create_user(db, user_params[0], user_params[1], verified=user_params[2])
	new_user_id = User.query.filter_by(username=user_params[0]['username']).first().id

	# if testing with a logged in user
	if loggin_user:
		login(app_client, user_params[0]['email'], user_params[0]['password'])

	response = app_client.get('/user/' + str(new_user_id))
	assert response.status_code == expect[0]
	# If user logged in then make sure their parameeters are as expected
	if current_user.is_authenticated:
		assert current_user.has_role(user_params[1]) == True
		if user_params[2]:
			assert current_user.has_role('verified') == True
		else:
			assert current_user.has_role('verified') == False
		assert current_user.id == new_user_id


@pytest.mark.parametrize("current_user_params, target_user_params, expect", [
	([ADMIN_USER, 'admin', True], [STANDARD_USER, 'standard', True], [200]),
	([ADMIN_USER, 'admin', False], [STANDARD_USER, 'standard', True], [402]),
	([ADMIN_USER, 'admin', True], [STANDARD_USER, 'standard', False], [200]),
	([ADMIN_USER, 'admin', False], [STANDARD_USER, 'standard', False], [402]),
	([ADMIN_USER, 'admin', False], [ADMIN_USER_2, 'admin', False], [402]),
	([ADMIN_USER, 'admin', False], [ADMIN_USER_2, 'admin', True], [402]),
	([ADMIN_USER, 'admin', True], [ADMIN_USER_2, 'admin', False], [200]),
	([ADMIN_USER, 'admin', True], [ADMIN_USER_2, 'admin', True], [200]),
	([STANDARD_USER, 'standard', False], [ADMIN_USER, 'admin', True], [402]),
	([STANDARD_USER, 'standard', True], [ADMIN_USER, 'admin', True], [402]),
	([STANDARD_USER, 'standard', False], [ADMIN_USER, 'admin', False], [402]),
	([STANDARD_USER, 'standard', True], [ADMIN_USER, 'admin', False], [402]),
	([STANDARD_USER, 'standard', False], [STANDARD_USER_2, 'standard', True], [402]),
	([STANDARD_USER, 'standard', True], [STANDARD_USER_2, 'standard', True], [402]),
	([STANDARD_USER, 'standard', False], [STANDARD_USER_2, 'standard', False], [402]),
	([STANDARD_USER, 'standard', True], [STANDARD_USER_2, 'standard', False], [402])
])
def test_user_profile_multi_user(db, app_client, current_user_params, target_user_params, expect):
	"""
	GIVEN a Flask application configured for testing and 2 standard users (verified)
	WHEN the '/user/<id>' page is requested (GET) for the non current_user
	THEN check that the response is 302
	"""
	create_user(db, current_user_params[0], current_user_params[1], verified=current_user_params[2])
	create_user(db, target_user_params[0], target_user_params[1], verified=target_user_params[2])
	login(app_client, current_user_params[0]['email'], current_user_params[0]['password'])

	target_user_id = User.query.filter_by(username=target_user_params[0]['username']).first().id

	response = app_client.get('/user/' + str(target_user_id))
	assert current_user.has_role(current_user_params[1]) == True
	if current_user_params[2]:
		assert current_user.has_role('verified') == True
	else:
		assert current_user.has_role('verified') == False


# Toggle user roles route

@pytest.mark.parametrize("current_user_params, subject_user_params, role_name, expect", [
	([ADMIN_USER, 'admin', True], [STANDARD_USER, 'standard', False], 'verified', [200, True]),
	([ADMIN_USER, 'admin', True], [STANDARD_USER, 'standard', True], 'verified', [200, False]),
	([ADMIN_USER, 'admin', True], [ADMIN_USER_2, 'admin', False], 'verified', [200, True]),
	([ADMIN_USER, 'admin', True], [ADMIN_USER_2, 'admin', True], 'verified', [200, False]),
	([ADMIN_USER, 'admin', True], [ADMIN_USER_2, 'admin', True], 'standard', [200, True]),
	([ADMIN_USER, 'admin', True], [STANDARD_USER, 'standard', False], 'admin', [200, True]),
	([ADMIN_USER, 'admin', False], [STANDARD_USER, 'standard', False], 'verified', [403, False]),
	([ADMIN_USER, 'admin', False], [STANDARD_USER, 'standard', True], 'verified', [403, True]),
	([ADMIN_USER, 'admin', False], [ADMIN_USER_2, 'admin', False], 'verified', [403, False]),
	([ADMIN_USER, 'admin', False], [ADMIN_USER_2, 'admin', True], 'verified', [403, True]),
	([STANDARD_USER, 'standard', True], [STANDARD_USER_2, 'standard', False], 'verified', [403, False]),
	([STANDARD_USER, 'standard', True], [STANDARD_USER_2, 'standard', True], 'verified', [403, True]),
	([STANDARD_USER, 'standard', False], [STANDARD_USER_2, 'standard', False], 'verified', [403, False]),
	([STANDARD_USER, 'standard', False], [STANDARD_USER_2, 'standard', True], 'verified', [403, True]),
	([STANDARD_USER, 'standard', True], [ADMIN_USER, 'admin', False], 'verified', [403, False]),
	([STANDARD_USER, 'standard', True], [ADMIN_USER, 'admin', True], 'verified', [403, True]),
	([STANDARD_USER, 'standard', False], [ADMIN_USER, 'admin', False], 'verified', [403, False]),
	([STANDARD_USER, 'standard', False], [ADMIN_USER, 'admin', True], 'verified', [403, True]),
])
def test_two_user_role_toggle(db, app_client, current_user_params, subject_user_params, role_name, expect):
	"""
	GIVEN a Flask application configured for testing and two users
	WHEN one user tries to toggle a role to the other user
	THEN only allow the action if the other user is an admin and verified

	parmas:
	current_user_params: [dict of user parameters, string user role, bool verifed]
	subject_user_params: [dict of user parameters, string user role, bool verifed]
	role_name: string role name to toggle
	expect: [int expected response code, bool expected role value]
	"""

	# make users and login
	create_user(db, current_user_params[0], current_user_params[1], verified=current_user_params[2])
	create_user(db, subject_user_params[0], subject_user_params[1], verified=subject_user_params[2])
	login(app_client, current_user_params[0]['email'], current_user_params[0]['password'])

	# get target user
	subject_user = User.query.filter_by(username=subject_user_params[0]['username']).first()

	# toggle role and make sure the status code and role are expected
	response = app_client.get('/user/' + str(subject_user.id) + '/toggle_role/' + role_name, follow_redirects=True)
	assert response.status_code == expect[0]
	assert subject_user.has_role(role_name) == expect[1]


@pytest.mark.parametrize("user_params, role_name, expect", [
	([ADMIN_USER, 'admin', True], 'standard', [403, False]),
	([ADMIN_USER, 'admin', True], 'admin', [403, True]),
	([ADMIN_USER, 'admin', False], 'standard', [403, False]),
	([ADMIN_USER, 'admin', False], 'verified', [403, False]),
	([STANDARD_USER, 'standard', True], 'admin', [403, False]),
	([STANDARD_USER, 'standard', True], 'standard', [403, True]),
	([STANDARD_USER, 'standard', False], 'admin', [403, False]),
	([STANDARD_USER, 'standard', False], 'verified', [403, False]),
])
def test_one_user_role_toggle(db, app_client, user_params, role_name, expect):
	"""
	GIVEN a Flask application configured for testing and a user
	WHEN the user tries to toggle a role for theirself
	THEN do not allow the action

	parmas:
	user_params: [dict of user parameters, string user role, bool verifed]
	role_name: string role name to toggle
	expect: [int expected response code, bool expected role value]
	"""

	# make user and login
	create_user(db, user_params[0], user_params[1], verified=user_params[2])
	login(app_client, user_params[0]['email'], user_params[0]['password'])

	# toggle role and make sure the status code and role are expected
	response = app_client.get('/user/' + str(current_user.id) + '/toggle_role/' + role_name, follow_redirects=True)
	assert response.status_code == expect[0]
	assert current_user.has_role(role_name) == expect[1]


@pytest.mark.parametrize("user_params, role_name, expect", [
	([ADMIN_USER, 'admin', True], 'standard', [302, False]),
	([ADMIN_USER, 'admin', True], 'admin', [302, True]),
	([STANDARD_USER, 'standard', False], 'verified', [302, False]),
	([STANDARD_USER, 'standard', True], 'admin', [302, False]),
])
def test_no_user_role_toggle(db, app_client, user_params, role_name, expect):
	"""
	GIVEN a Flask application configured for testing
	WHEN no user tries to toggle a role for a user
	THEN do not allow the action

	parmas:
	user_params: [dict of user parameters, string user role, bool verifed]
	role_name: string role name to toggle
	expect: [int expected response code, bool expected role value]
	"""

	# make user but DO NOT login
	create_user(db, user_params[0], user_params[1], verified=user_params[2])

	# get target user
	subject_user = User.query.filter_by(username=user_params[0]['username']).first()

	# toggle role and make sure the status code and role are expected
	response = app_client.get('/user/' + str(subject_user.id) + '/toggle_role/' + role_name)
	assert subject_user.has_role(role_name) == expect[1]
	assert response.status_code == expect[0]
	assert b"login" in response.data  # WE expect to find login as this test assumes no user is logged in
