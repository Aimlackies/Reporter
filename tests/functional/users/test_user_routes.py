from conftest import app_client, STANDARD_USER, ADMIN_USER, db
from utils import create_user, login
from reporter_app.models import Role, User
import pytest
from flask_security import current_user
from sqlalchemy.sql import func
import secrets


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

def test_users_page_no_user(app_client):
	"""
	GIVEN a Flask application configured for testing and no user
	WHEN the '/users/' page is requested (GET)
	THEN check that the response is 302 and redirected to login page
	"""
	response = app_client.get('/users/')
	assert response.status_code == 302
	assert b"login" in response.data
	assert b"Redirecting..." in response.data


def test_users_page_admin_user(db, app_client):
	"""
	GIVEN a Flask application configured for testing and admin user (verified)
	WHEN the '/users/' page is requested (GET)
	THEN check that the response is 200
	"""
	create_user(db, ADMIN_USER, 'admin')
	login(app_client, ADMIN_USER['email'], ADMIN_USER['password'])

	response = app_client.get('/users/')
	assert response.status_code == 200
	assert b"<h1 class=\"h2\">Users</h1>" in response.data
	assert current_user.has_role('admin') == True
	assert current_user.has_role('standard') == False
	assert current_user.has_role('verified') == True
	assert len(current_user.roles) == 2  # verified and admin


def test_users_page_standard_user(db, app_client):
	"""
	GIVEN a Flask application configured for testing and standard user (verified)
	WHEN the '/users/' page is requested (GET)
	THEN check that the response is 403 and redirected to 403 page
	"""
	create_user(db, STANDARD_USER, 'standard')
	login(app_client, STANDARD_USER['email'], STANDARD_USER['password'])

	response = app_client.get('/users/')
	assert response.status_code == 403
	assert b"<h1>403" in response.data
	assert current_user.has_role('standard') == True
	assert current_user.has_role('admin') == False
	assert current_user.has_role('verified') == True
	assert len(current_user.roles) == 2  # verified and standard


def test_users_page_admin_user_unverified(db, app_client):
	"""
	GIVEN a Flask application configured for testing and admin user (unverified)
	WHEN the '/users/' page is requested (GET)
	THEN check that the response is 403 and redirected to 403 page
	"""
	create_user(db, ADMIN_USER, 'admin', verified=False)
	login(app_client, ADMIN_USER['email'], ADMIN_USER['password'])

	response = app_client.get('/users/')
	assert response.status_code == 403
	assert b"<h1>403" in response.data
	assert current_user.has_role('admin') == True
	assert current_user.has_role('standard') == False
	assert current_user.has_role('verified') == False
	assert len(current_user.roles) == 1  # admin


def test_users_page_standard_user_unverified(db, app_client):
	"""
	GIVEN a Flask application configured for testing and standard user (unverified)
	WHEN the '/users/' page is requested (GET)
	THEN check that the response is 403 and redirected to 403 page
	"""
	create_user(db, STANDARD_USER, 'standard', verified=False)
	login(app_client, STANDARD_USER['email'], STANDARD_USER['password'])

	response = app_client.get('/users/')
	assert response.status_code == 403
	assert b"<h1>403" in response.data
	assert current_user.has_role('standard') == True
	assert current_user.has_role('admin') == False
	assert current_user.has_role('verified') == False
	assert len(current_user.roles) == 1  # standard

# User profile page


def test_userID_page_no_user(db, app_client):
	"""
	GIVEN a Flask application configured for testing and a standard user
	WHEN the '/user/<id>' page is requested (GET)
	THEN check that the response is 302 and redirected to login page
	"""
	create_user(db, STANDARD_USER, 'standard', verified=True)
	new_user_id = User.query.filter_by(username=STANDARD_USER['username']).first().id

	response = app_client.get('/user/' + str(new_user_id))
	assert response.status_code == 302
	assert b"login" in response.data
	assert b"Redirecting..." in response.data


def test_userID_page_for_current_user_standard(db, app_client):
	"""
	GIVEN a Flask application configured for testing and standard user (verified)
	WHEN the '/user/<id>' page is requested (GET)
	THEN check that the response is 200
	"""
	create_user(db, STANDARD_USER, 'standard', verified=True)
	login(app_client, STANDARD_USER['email'], STANDARD_USER['password'])

	response = app_client.get('/user/' + str(current_user.id))
	assert response.status_code == 200
	assert b"<h1 class=\"h2\">Profile</h1>" in response.data
	assert current_user.has_role('admin') == False
	assert current_user.has_role('standard') == True
	assert current_user.has_role('verified') == True


def test_userID_page_for_current_user_standard_unverified(db, app_client):
	"""
	GIVEN a Flask application configured for testing and standard user (unverifed)
	WHEN the '/user/<id>' page is requested (GET)
	THEN check that the response is 200
	"""
	create_user(db, STANDARD_USER, 'standard', verified=False)
	login(app_client, STANDARD_USER['email'], STANDARD_USER['password'])

	response = app_client.get('/user/' + str(current_user.id))
	assert response.status_code == 200
	assert b"<h1 class=\"h2\">Profile</h1>" in response.data
	assert current_user.has_role('admin') == False
	assert current_user.has_role('standard') == True
	assert current_user.has_role('verified') == False


def test_userID_page_for_current_user_admin(db, app_client):
	"""
	GIVEN a Flask application configured for testing and admin user (verifed)
	WHEN the '/user/<id>' page is requested (GET)
	THEN check that the response is 200
	"""
	create_user(db, ADMIN_USER, 'admin', verified=True)
	login(app_client, ADMIN_USER['email'], ADMIN_USER['password'])

	response = app_client.get('/user/' + str(current_user.id))
	assert response.status_code == 200
	assert b"<h1 class=\"h2\">Profile</h1>" in response.data
	assert current_user.has_role('admin') == True
	assert current_user.has_role('standard') == False
	assert current_user.has_role('verified') == True


def test_userID_page_for_current_user_admin_unverified(db, app_client):
	"""
	GIVEN a Flask application configured for testing and admin user (unverifed)
	WHEN the '/user/<id>' page is requested (GET)
	THEN check that the response is 200
	"""
	create_user(db, ADMIN_USER, 'admin', verified=False)
	login(app_client, ADMIN_USER['email'], ADMIN_USER['password'])

	response = app_client.get('/user/' + str(current_user.id))
	assert response.status_code == 200
	assert b"<h1 class=\"h2\">Profile</h1>" in response.data
	assert current_user.has_role('admin') == True
	assert current_user.has_role('standard') == False
	assert current_user.has_role('verified') == False


def test_userID_page_for_non_current_user_standard(db, app_client):
	"""
	GIVEN a Flask application configured for testing and 2 standard users (verified)
	WHEN the '/user/<id>' page is requested (GET) for the non current_user
	THEN check that the response is 302
	"""
	create_user(db, STANDARD_USER, 'standard', verified=True)
	create_user(db, STANDARD_USER_2, 'standard', verified=True)

	login(app_client, STANDARD_USER['email'], STANDARD_USER['password'])

	new_user_id = User.query.filter_by(username=STANDARD_USER_2['username']).first().id

	response = app_client.get('/user/' + str(new_user_id))
	assert response.status_code == 302
	assert b"redirected automatically to target URL: <a href=\"/dashboard\">" in response.data
	assert current_user.has_role('admin') == False
	assert current_user.has_role('standard') == True
	assert current_user.has_role('verified') == True


def test_userID_page_for_non_current_user_standard_unverified(db, app_client):
	"""
	GIVEN a Flask application configured for testing and 2 standard users (unverified)
	WHEN the '/user/<id>' page is requested (GET) for the non current_user
	THEN check that the response is 302
	"""
	create_user(db, STANDARD_USER, 'standard', verified=False)
	create_user(db, STANDARD_USER_2, 'standard', verified=True)

	login(app_client, STANDARD_USER['email'], STANDARD_USER['password'])

	new_user_id = User.query.filter_by(username=STANDARD_USER_2['username']).first().id

	response = app_client.get('/user/' + str(new_user_id))
	assert response.status_code == 302
	assert b"redirected automatically to target URL: <a href=\"/dashboard\">" in response.data
	assert current_user.has_role('admin') == False
	assert current_user.has_role('standard') == True
	assert current_user.has_role('verified') == False


def test_userID_page_for_non_current_user_admin(db, app_client):
	"""
	GIVEN a Flask application configured for testing and 1 standard users + 1 admin user (verified)
	WHEN the '/user/<id>' page is requested (GET) for the standard user by the admin user
	THEN check that the response is 200
	"""
	create_user(db, STANDARD_USER, 'standard', verified=True)
	create_user(db, ADMIN_USER, 'admin', verified=True)

	login(app_client, ADMIN_USER['email'], ADMIN_USER['password'])

	new_user_id = User.query.filter_by(username=STANDARD_USER['username']).first().id

	response = app_client.get('/user/' + str(new_user_id))
	assert response.status_code == 200
	assert b"<h1 class=\"h2\">Profile</h1>" in response.data
	assert current_user.has_role('admin') == True
	assert current_user.has_role('standard') == False
	assert current_user.has_role('verified') == True


def test_userID_page_for_non_current_user_admin_unverified(db, app_client):
	"""
	GIVEN a Flask application configured for testing and 1 standard users + 1 admin user (unverified)
	WHEN the '/user/<id>' page is requested (GET) for the standard user by the admin user
	THEN check that the response is 302
	"""
	create_user(db, STANDARD_USER, 'standard', verified=True)
	create_user(db, ADMIN_USER, 'admin', verified=False)

	login(app_client, ADMIN_USER['email'], ADMIN_USER['password'])

	new_user_id = User.query.filter_by(username=STANDARD_USER['username']).first().id

	response = app_client.get('/user/' + str(new_user_id))
	assert response.status_code == 302
	assert b"redirected automatically to target URL: <a href=\"/dashboard\">" in response.data
	assert current_user.has_role('admin') == True
	assert current_user.has_role('standard') == False
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
def test_two_user_role_toggle(db, app_client, user_params, role_name, expect):
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
