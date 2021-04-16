from conftest import app_client, STANDARD_USER, ADMIN_USER, db
from reporter_app.models import Role, User
import pytest
from flask_security import current_user

from reporter_app.models import User


def login(client, email, password):
	return client.post('/login', data=dict(
		email=email,
		password=password
	), follow_redirects=True)


def create_user(db, user_dict, role_name):
	db.session.add(User(
		username=user_dict['username'],
		first_name=user_dict['first_name'],
		surname=user_dict['surname'],
		email=user_dict['email'],
		password=user_dict['password'],
		confirmed_at=user_dict['confirmed_at'],
		fs_uniquifier=user_dict['fs_uniquifier'],
		active=user_dict['active']
	))

	db.session.commit()
	standard_user = User.query.filter_by(email=user_dict['email']).first()
	standard_role = Role.query.filter_by(name=role_name).first()
	standard_user.roles.append(standard_role)
	db.session.commit()


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


def test_dashboard_page_admin_user(app_client):
	"""
	GIVEN a Flask application configured for testing and admin user (verified)
	WHEN the '/' page is requested (GET)
	THEN check that the response is 302 and redirected to login page
	"""
	pass


def test_dashboard_page_standard_user(app_client):
	"""
	GIVEN a Flask application configured for testing and standard user (verified)
	WHEN the '/' page is requested (GET)
	THEN check that the response is 302 and redirected to login page
	"""
	pass


def test_dashboard_page_standard_user_unverified(app_client):
	"""
	GIVEN a Flask application configured for testing and standard user (unverified)
	WHEN the '/' page is requested (GET)
	THEN check that the response is XXX and redirected to login page
	"""
	pass


def test_dashboard_page_admin_user_unverified(app_client):
	"""
	GIVEN a Flask application configured for testing and admin user (unverified)
	WHEN the '/' page is requested (GET)
	THEN check that the response is XXX and redirected to login page
	"""
	pass


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
	assert current_user.roles[0].name == "admin"
	assert len(current_user.roles) == 1


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
	assert current_user.roles[0].name == "standard"
	assert len(current_user.roles) == 1
