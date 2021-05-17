from conftest import app_client, STANDARD_USER, ADMIN_USER, db
from utils import create_user, login
from reporter_app.models import Role, User
import pytest
from flask_security import current_user

from reporter_app.models import User


def test_login_page_no_user(app_client):
	"""
	GIVEN a Flask application configured for testing and no user
	WHEN the '/login' page is requested (GET)
	THEN check that the response is 200
	"""

	response = app_client.get('/login')
	assert response.status_code == 200
	assert b"form action=\"/login\"" in response.data
	assert current_user.is_authenticated == False  # No user currently logged in


def test_login_page_admin_user(db, app_client):
	"""
	GIVEN a Flask application configured for testing and admin user
	WHEN the '/login' page is requested (GET)
	THEN check that the response is 302 and redirected to dashboard page
	"""

	create_user(db, ADMIN_USER, 'admin')
	login(app_client, ADMIN_USER['email'], ADMIN_USER['password'])

	response = app_client.get('/login')
	assert response.status_code == 302
	assert b"Redirecting..." in response.data
	assert b"href=\"/\"" in response.data
	assert current_user.has_role('admin') == True
	assert current_user.has_role('standard') == False
	assert len(current_user.roles) == 2  # verified and admin


def test_login_page_standard_user(db, app_client):
	"""
	GIVEN a Flask application configured for testing and standard user
	WHEN the '/login' page is requested (GET)
	THEN check that the response is 302 and redirected to dashboard page
	"""

	create_user(db, STANDARD_USER, 'standard')
	login(app_client, STANDARD_USER['email'], STANDARD_USER['password'])

	response = app_client.get('/login')
	assert response.status_code == 302
	assert b"Redirecting..." in response.data
	assert b"href=\"/\"" in response.data
	assert current_user.has_role('standard') == True
	assert current_user.has_role('admin') == False
	assert len(current_user.roles) == 2  # verified and standard
