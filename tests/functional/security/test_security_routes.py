from conftest import app_client, STANDARD_USER, ADMIN_USER, db
from utils import create_user, login, get_register_params
from reporter_app.models import Role, User
import pytest
from flask_security import current_user
import json
from reporter_app.models import User


# Login

@pytest.mark.parametrize("user_params, expect", [
	([ADMIN_USER, 'admin', True], [302]),
	([ADMIN_USER, 'admin', False], [302]),
	([STANDARD_USER, 'standard', True], [302]),
	([STANDARD_USER, 'standard', False], [302]),
	(None, [200]),
])
def test_login_get(db, app_client, user_params, expect):
	"""
	GIVEN a Flask application configured for testing and zero or one user parameters
	WHEN the '/login' page is requested (GET)
	THEN if a user is provided redirect, otherwise allow the request

	parmas:
	user_params: [dict of user parameters, string user role, bool verifed]
	expect: [int expected response code]
	"""

	if user_params != None:
		create_user(db, user_params[0], user_params[1], verified=user_params[2])
		login(app_client, user_params[0]['email'], user_params[0]['password'])

	response = app_client.get('/login')
	assert response.status_code == expect[0]
	if user_params != None:
		assert current_user.is_authenticated == True  # User currently logged in
		assert current_user.has_role(user_params[1]) == True
	else:
		assert current_user.is_authenticated == False  # No user currently logged in


@pytest.mark.parametrize("user_params, login_params, expect", [
	([ADMIN_USER, 'admin', True], None, [302, True]),  # 302 as user is redirected after login
	([ADMIN_USER, 'admin', False], None, [302, True]),  # 302 as user is redirected after login
	([STANDARD_USER, 'standard', True], None, [302, True]),  # 302 as user is redirected after login
	([STANDARD_USER, 'standard', False], None, [302, True]),  # 302 as user is redirected after login
	([STANDARD_USER, 'standard', True], {"email": "other@test.com", "password": "password"}, [200, False]),  # Response is 200 as login page reloads
	([STANDARD_USER, 'standard', False], {"email": "", "password": ""}, [200, False]),  # Response is 200 as login page reloads
	([STANDARD_USER, 'admin', False], {"email": None, "password": None}, [200, False]),  # Response is 200 as login page reloads
])
def test_login_post(db, app_client, user_params, login_params, expect):
	"""
	GIVEN a Flask application configured for testing and zero or one user parameters
	WHEN the '/login' page is sent form data (POST)
	THEN if a user is logged in their request sould be declined, otherwise login the user

	parmas:
	user_params: [dict of user parameters, string user role, bool verifed]
	login_params: dict of email and password if differnt to user created; else None
	expect: [int expected response code, bool user loged in]
	"""

	if user_params != None:
		create_user(db, user_params[0], user_params[1], verified=user_params[2])

	# If loging into the user created
	if login_params == None:
		data = {
			'email': user_params[0]['email'],
			'password': user_params[0]['password']
		}
	# If not loging into the user created
	else:
		data = {
			'email': login_params['email'],
			'password': login_params['password']
		}

	response = app_client.post('/login', data=data)
	assert response.status_code == expect[0]
	if expect[1]:
		assert current_user.is_authenticated == True  # User currently logged in
		assert current_user.email == user_params[0]['email']
		assert current_user.has_role(user_params[1]) == True
	else:
		assert current_user.is_authenticated == False  # No user currently logged in
		assert user_params[0]['email'] != login_params['email']


# Logout

@pytest.mark.parametrize("user_params, expect", [
	([ADMIN_USER, 'admin', True], [302]),
	([ADMIN_USER, 'admin', False], [302]),
	([STANDARD_USER, 'standard', True], [302]),
	([STANDARD_USER, 'standard', False], [302]),
	(None, [302])  # no user is redirected to login
])
def test_logout_get(db, app_client, user_params, expect):
	"""
	GIVEN a Flask application configured for testing and zero or one user parameters
	WHEN the '/logout' page is sent form data (GET)
	THEN if a user is logged in their request sould be accepted, otherwise declined

	parmas:
	user_params: [dict of user parameters, string user role, bool verifed]; else None
	expect: [int expected response code, bool user loged in]
	"""

	if user_params != None:
		create_user(db, user_params[0], user_params[1], verified=user_params[2])
		login(app_client, user_params[0]['email'], user_params[0]['password'])

	if user_params != None:
		assert current_user.is_authenticated == True
	else:
		app_client.get('/')  # If no user is logged in then there needs to be some interaction with the client to initilise the anonymous user
		assert current_user.is_authenticated == False
	response = app_client.get('/logout')
	assert response.status_code == expect[0]
	assert current_user.is_authenticated == False

# register page


@pytest.mark.parametrize("user_params, expect", [
	([ADMIN_USER, 'admin', True], [302]),
	([ADMIN_USER, 'admin', False], [302]),
	([STANDARD_USER, 'standard', True], [302]),
	([STANDARD_USER, 'standard', False], [302]),
	(None, [200]),
])
def test_register_get(db, app_client, user_params, expect):
	"""
	GIVEN a Flask application configured for testing and zero or one user parameters
	WHEN the '/register' page is requested (GET)
	THEN if a user is provided redirect, otherwise allow the request

	parmas:
	user_params: [dict of user parameters, string user role, bool verifed]
	expect: [int expected response code]
	"""

	if user_params != None:
		create_user(db, user_params[0], user_params[1], verified=user_params[2])
		login(app_client, user_params[0]['email'], user_params[0]['password'])

	response = app_client.get('/register')
	assert response.status_code == expect[0]
	if user_params != None:
		assert current_user.is_authenticated == True  # User currently logged in
		assert current_user.has_role(user_params[1]) == True
	else:
		assert current_user.is_authenticated == False  # No user currently logged in


@pytest.mark.parametrize("user_params, change, expect", [
	(get_register_params("standard"), {"drop": False, "param": "email", "value": "a@b.com"}, {"user_count": 1, "error_msg": None, "code": 302}),  # create successful user
	(get_register_params("standard"), {"drop": False, "param": "password", "value": "differentPassword"}, {"user_count": 0, "error_msg": "Passwords do not match", "code": 200}),
	(get_register_params("standard"), {"drop": False, "param": "email", "value": "notAnEmail"}, {"user_count": 0, "error_msg": "Invalid email address", "code": 200}),
	(get_register_params("admin"), {"drop": False, "param": "email", "value": "com.emial@test"}, {"user_count": 0, "error_msg": "Invalid email address", "code": 200}),
	(get_register_params("admin"), {"drop": False, "param": "email", "value": "@test.com"}, {"user_count": 0, "error_msg": "Invalid email address", "code": 200}),
	(get_register_params("admin"), {"drop": False, "param": "email", "value": "hello.com"}, {"user_count": 0, "error_msg": "Invalid email address", "code": 200}),
	(get_register_params("admin"), {"drop": False, "param": "email", "value": "email@...com"}, {"user_count": 0, "error_msg": "Invalid email address", "code": 200}),
	(get_register_params("admin"), {"drop": False, "param": "email", "value": "someCallMe@Tim"}, {"user_count": 0, "error_msg": "Invalid email address", "code": 200}),
	(get_register_params("admin"), {"drop": False, "param": "email", "value": "a"*(64) + "@a.com"}, {"user_count": 1, "error_msg": None, "code": 302}),
	(get_register_params("admin"), {"drop": False, "param": "email", "value": "a"*(65) + "@a.com"}, {"user_count": 0, "error_msg": "Invalid email address", "code": 200}),
	(get_register_params("standard"), {"drop": False, "param": "email", "value": "a"*(1) + "@a.com"}, {"user_count": 1, "error_msg": None, "code": 302}),
	(get_register_params("standard"), {"drop": False, "param": "email", "value": "a"*64 + "@" + "a"*64 + ".com"}, {"user_count": 0, "error_msg": "Invalid email address", "code": 200}),
	(get_register_params("standard"), {"drop": False, "param": "email", "value": "a"*64 + "@" + "a"*63 + ".com"}, {"user_count": 1, "error_msg": None, "code": 302}),  # email tests should only be checking the len of an email address, not the lengh of each section. This will be set in Flask Security Too somewhere
	(get_register_params("standard"), {"drop": False, "param": "first_name", "value": "a"*255}, {"user_count": 1, "error_msg": None, "code": 302}),
	(get_register_params("standard"), {"drop": False, "param": "first_name", "value": "a"*1}, {"user_count": 1, "error_msg": None, "code": 302}),
])
def test_register_parameters(db, app_client, user_params, change, expect):
	"""
	GIVEN a Flask application configured for testing and zero or one user parameters
	WHEN the '/register' page is requested (POST)
	THEN the provided user parameters are accepted then create a new user, else return an appropraite error message

	parmas:
	user_params: dict of user parameters
	change: dict{
		drop: True if param to change is to be removed, else False
		param: string parameter name to alter
		value: value to chame param value to (only use if drop == False)
	}
	expect: dict{
		user_count: [int number of users expected, string parmeter filter by ("username" or "email")]
		error_msg: String of error message to expect, else None if no error expected
		code: expected error code
	}
	"""

	if change["drop"]:
		del user_params[change["param"]]
	else:
		user_params[change["param"]] = change["value"]

	data = {
		**user_params
	}

	response = app_client.post('/register', data=data)
	assert response.status_code == expect["code"]

	if expect["error_msg"] != None:
		assert expect["error_msg"] in str(response.data)
	assert User.query.filter_by(email=user_params["email"]).count() == expect["user_count"]

# reset password page
