from conftest import test_client, init_database, new_admin_user, new_standard_user
import pytest
from flask_security import current_user

from reporter_app.models import User


def login(client, email, password):
	return client.post('/login', data=dict(
		email=email,
		password=password
	), follow_redirects=True)

def test_dashboard_page_no_user(test_client):
	"""
	GIVEN a Flask application configured for testing and no user
	WHEN the '/' page is requested (GET)
	THEN check that the response is 302 and redirected to login page
	"""
	response = test_client.get('/')
	assert response.status_code == 302
	assert b"login" in response.data
	assert b"Redirecting..." in response.data


def test_dashboard_page_admin_user(test_client, new_admin_user):
	"""
	GIVEN a Flask application configured for testing and admin user (verified)
	WHEN the '/' page is requested (GET)
	THEN check that the response is 302 and redirected to login page
	"""
	pass


def test_dashboard_page_standard_user(test_client, new_standard_user):
	"""
	GIVEN a Flask application configured for testing and standard user (verified)
	WHEN the '/' page is requested (GET)
	THEN check that the response is 302 and redirected to login page
	"""
	pass


def test_dashboard_page_standard_user_unverified(test_client, new_standard_user):
	"""
	GIVEN a Flask application configured for testing and standard user (unverified)
	WHEN the '/' page is requested (GET)
	THEN check that the response is XXX and redirected to login page
	"""
	pass


def test_dashboard_page_admin_user_unverified(test_client, new_admin_user):
	"""
	GIVEN a Flask application configured for testing and admin user (unverified)
	WHEN the '/' page is requested (GET)
	THEN check that the response is XXX and redirected to login page
	"""
	pass


#@pytest.mark.parametrize("response_expect, data_expect_include", [
#	(None, 200, b"form action=\"/login\""),
#	(new_admin_user, 200, b"form action=\"/login\""),
#	(new_standard_user, 200, b"form action=\"/login\"")
#])
def test_login_page_no_user(test_client, init_database):
	"""
	GIVEN a Flask application configured for testing and no user
	WHEN the '/login' page is requested (GET)
	THEN check that the response is 200
	"""

	response = test_client.get('/login')
	assert response.status_code == 200
	assert b"form action=\"/login\"" in response.data
	assert current_user.is_authenticated == False  # No user currently logged in


def test_login_page_admin_user(test_client, init_database, new_admin_user):
	"""
	GIVEN a Flask application configured for testing and admin user
	WHEN the '/login' page is requested (GET)
	THEN check that the response is 302 and redirected to dashboard page
	"""

	user = new_admin_user

	response = test_client.post('/login', data=dict(
		email=user.email,
		password=user.password
	), follow_redirects=True)

	response = test_client.get('/login')
	assert response.status_code == 302
	assert b"Redirecting..." in response.data
	assert b"href=\"/\"" in response.data
	assert current_user.roles[0].name == "admin"
	assert len(current_user.roles) == 1

	test_client.get('/logout')  # This is required to rest the session to default


def test_login_page_standard_user(test_client, init_database, new_standard_user):
	"""
	GIVEN a Flask application configured for testing and standard user
	WHEN the '/login' page is requested (GET)
	THEN check that the response is 302 and redirected to dashboard page
	"""

	user = new_standard_user

	response = test_client.post('/login', data=dict(
		email=user.email,
		password=user.password
	), follow_redirects=True)

	response = test_client.get('/login')
	assert response.status_code == 302
	assert b"Redirecting..." in response.data
	assert b"href=\"/\"" in response.data
	assert current_user.roles[0].name == "standard"
	assert len(current_user.roles) == 1

	test_client.get('/logout')  # This is required to rest the session to default
