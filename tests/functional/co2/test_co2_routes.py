from conftest import app_client, STANDARD_USER, ADMIN_USER, db
from utils import create_user, login
from reporter_app.models import Role, User
import pytest
from flask_security import current_user


@pytest.mark.parametrize("user_params, expect", [
	([ADMIN_USER, 'admin', True], [200]),
	([ADMIN_USER, 'admin', False], [403]),
	([STANDARD_USER, 'standard', True], [200]),
	([STANDARD_USER, 'standard', False], [403]),
	(None, [302]),
])
def test_co2_page(db, app_client, user_params, expect):
	"""
	GIVEN a Flask application configured for testing and zero or one user parameters
	WHEN the '/co2' page is requested (GET)
	THEN make sure only verified users can access it and correct status code for all access attempts

	parmas:
	user_params: [dict of user parameters, string user role, bool verifed]
	expect: [int expected response code]
	"""
	if user_params != None:
		create_user(db, user_params[0], user_params[1], verified=user_params[2])
		login(app_client, user_params[0]['email'], user_params[0]['password'])

	response = app_client.get('/co2', follow_redirects=False)
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
