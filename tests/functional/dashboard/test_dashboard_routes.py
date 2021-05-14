from conftest import app_client, STANDARD_USER, ADMIN_USER, db
from utils import create_user, login
from reporter_app.models import Role, User
import pytest
from flask_security import current_user

from reporter_app.models import User


def test_dashboard_page_no_user(app_client):
	"""
	GIVEN a Flask application configured for testing and no user
	WHEN the '/' page is requested (GET)
	THEN check that the response is 302 and redirected to login page
	"""
	response = app_client.get('/')
	assert response.status_code == 302
	assert b"login" in response.data
	assert b"Redirecting..." in response.data


def test_dashboard_page_admin_user(db, app_client):
	"""
	GIVEN a Flask application configured for testing and admin user (verified)
	WHEN the '/' page is requested (GET)
	THEN check that the response is 200
	"""
	create_user(db, ADMIN_USER, 'admin')
	login(app_client, ADMIN_USER['email'], ADMIN_USER['password'])

	response = app_client.get('/')
	assert response.status_code == 200
	assert b"<h1 class=\"h2\">Dashboard</h1>" in response.data
	assert current_user.has_role('admin') == True
	assert current_user.has_role('standard') == False
	assert len(current_user.roles) == 2  # verified and admin


def test_dashboard_page_standard_user(db, app_client):
	"""
	GIVEN a Flask application configured for testing and standard user (verified)
	WHEN the '/' page is requested (GET)
	THEN check that the response is 200
	"""
	create_user(db, STANDARD_USER, 'standard')
	login(app_client, STANDARD_USER['email'], STANDARD_USER['password'])

	response = app_client.get('/')
	assert response.status_code == 200
	assert b"<h1 class=\"h2\">Dashboard</h1>" in response.data
	assert current_user.has_role('standard') == True
	assert current_user.has_role('admin') == False
	assert len(current_user.roles) == 2  # verified and standard


def test_dashboard_page_admin_user_unverified(db, app_client):
	"""
	GIVEN a Flask application configured for testing and admin user (unverified)
	WHEN the '/' page is requested (GET)
	THEN check that the response is 403 and redirected to login page
	"""
	create_user(db, ADMIN_USER, 'admin', verified=False)
	login(app_client, ADMIN_USER['email'], ADMIN_USER['password'])

	response = app_client.get('/')
	assert response.status_code == 403
	assert b"<h1>403" in response.data
	assert current_user.has_role('admin') == True
	assert current_user.has_role('standard') == False
	assert current_user.has_role('verified') == False
	assert len(current_user.roles) == 1  # admin


def test_dashboard_page_standard_user_unverified(db, app_client):
	"""
	GIVEN a Flask application configured for testing and standard user (unverified)
	WHEN the '/' page is requested (GET)
	THEN check that the response is 403 and redirected to login page
	"""
	create_user(db, STANDARD_USER, 'standard', verified=False)
	login(app_client, STANDARD_USER['email'], STANDARD_USER['password'])

	response = app_client.get('/')
	assert response.status_code == 403
	assert b"<h1>403" in response.data
	assert current_user.has_role('standard') == True
	assert current_user.has_role('admin') == False
	assert current_user.has_role('verified') == False
	assert len(current_user.roles) == 1  # standard
