from conftest import app_client, STANDARD_USER, ADMIN_USER, db
from utils import create_user
from reporter_app.models import Role, User
import pytest
from flask_security import current_user

from reporter_app.models import User


def test_create_valid_user(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a valid user
	THEN check the transaction has been a successand the user is in the DB
	"""
	print(STANDARD_USER)
	db.session.add(User(
		username=STANDARD_USER['username'],
		first_name=STANDARD_USER['first_name'],
		surname=STANDARD_USER['surname'],
		password=STANDARD_USER['password'],
		confirmed_at=STANDARD_USER['confirmed_at'],
		fs_uniquifier=STANDARD_USER['fs_uniquifier'],
		active=STANDARD_USER['active']
	))

	response = app_client.get('/login')
	assert response.status_code == 302
	assert b"Redirecting..." in response.data
	assert b"href=\"/\"" in response.data
	assert current_user.roles[0].name == "admin"
	assert len(current_user.roles) == 1
