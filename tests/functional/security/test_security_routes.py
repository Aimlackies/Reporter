from conftest import app_client, STANDARD_USER, ADMIN_USER, db
from utils import create_user, login
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

# register page

# reset password page

# verify page
