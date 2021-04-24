from conftest import app_client, STANDARD_USER, ADMIN_USER, db
from utils import create_user, get_admin_user, get_standard_user
from reporter_app.models import Role, User
import pytest
from flask_security import current_user
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from reporter_app.models import User


def test_create_valid_user(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a valid user
	THEN check the transaction has been a successand the user is in the DB
	"""

	user = get_standard_user()

	db.session.add(User(
		username=user['username'],
		first_name=user['first_name'],
		surname=user['surname'],
		email=user['email'],
		password=user['password'],
		confirmed_at=user['confirmed_at'],
		fs_uniquifier=user['fs_uniquifier'],
		active=user['active']
	))

	db.session.commit()

	assert User.query.filter_by(username=STANDARD_USER['username']).count() == 1  # user does not exist


def test_create_user_missing_email(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a user without an email
	THEN check the transaction has been a unsuccessful for the email parameter and the user is not in the DB
	"""

	user = get_standard_user()

	db.session.begin_nested()
	with pytest.raises(IntegrityError) as e:
		db.session.add(User(
			username="user_missing_email",
			first_name=user['first_name'],
			surname=user['surname'],
			password=user['password'],
			confirmed_at=user['confirmed_at'],
			fs_uniquifier=user['fs_uniquifier'],
			active=user['active']
		))

		db.session.commit()
	db.session.rollback()

	assert "NOT NULL constraint failed: user.email" in str(e.value)  # email missing
	assert User.query.filter_by(username="user_missing_email").count() == 0  # user does not exist


def test_create_user_email_not_unique(db, app_client):
	"""
	GIVEN a Flask application configured for testing and a user already created
	WHEN submitting a transaction to create a user after a user with the same email exists
	THEN check the transaction has been a unsuccessful for the email parameter and the user is not in the DB
	"""

	not_unique_user_1 = get_standard_user()
	not_unique_user_1["username"] = "not_unique_user_1"
	not_unique_user_1["email"] = "email@email.com"
	not_unique_user_2 = get_standard_user()
	not_unique_user_2["username"] = "not_unique_user_2"
	not_unique_user_2["email"] = "email@email.com"

	db.session.add(User(
		username=not_unique_user_1['username'],
		first_name=not_unique_user_1['first_name'],
		surname=not_unique_user_1['surname'],
		email=not_unique_user_1['email'],
		password=not_unique_user_1['password'],
		confirmed_at=not_unique_user_1['confirmed_at'],
		fs_uniquifier=not_unique_user_1['fs_uniquifier'],
		active=not_unique_user_1['active']
	))
	db.session.commit()

	db.session.begin_nested()
	with pytest.raises(IntegrityError) as e:
		db.session.add(User(
			username=not_unique_user_2['username'],
			first_name=not_unique_user_2['first_name'],
			surname=not_unique_user_2['surname'],
			email=not_unique_user_2['email'],
			password=not_unique_user_2['password'],
			confirmed_at=not_unique_user_2['confirmed_at'],
			fs_uniquifier=not_unique_user_2['fs_uniquifier'],
			active=not_unique_user_2['active']
		))

		db.session.commit()
	db.session.rollback()

	assert "UNIQUE constraint failed: user.email" in str(e.value)  # email not unique
	assert User.query.filter_by(email="email@email.com").count() == 1  # Only one yesr exists
	assert User.query.filter_by(email="email@email.com").first().username == "not_unique_user_1" # First user that was created still exists


def test_create_user_email_max_length(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a user with an email of the maximum length
	THEN check the transaction has been successful and the user is in the DB
	"""

	user = get_standard_user()
	email_suffix = "@email.com"
	user['email'] = ("a" * (255 - len(email_suffix))) + email_suffix

	db.session.add(User(
		username=user['username'],
		first_name=user['first_name'],
		surname=user['surname'],
		password=user['password'],
		email=user['email'],
		confirmed_at=user['confirmed_at'],
		fs_uniquifier=user['fs_uniquifier'],
		active=user['active']
	))

	db.session.commit()

	assert len(user['email']) == 255
	assert User.query.filter_by(email=user['email']).count() == 1  # user does not exist


def test_create_user_email_over_max_length(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a user with an email over the maximum length
	THEN check the transaction has been a unsuccessful for the email parameter and the user is not in the DB
	"""

	# This does not work at the mement due to useing SQlite for testing. FIX ME!

	user = get_standard_user()
	email_suffix = "@email.com"
	user['email'] = ("a" * (255 - len(email_suffix) + 1)) + email_suffix

	print(user['email'])
	print(len(user['email']))

	db.session.begin_nested()
	with pytest.raises(IntegrityError) as e:
		db.session.add(User(
			username=user['username'],
			first_name=user['first_name'],
			surname=user['surname'],
			password=user['password'],
			email=user['email'],
			confirmed_at=user['confirmed_at'],
			fs_uniquifier=user['fs_uniquifier'],
			active=user['active']
		))

		db.session.commit()
	db.session.rollback()

	assert len(user['email']) == 256
	assert "NOT NULL constraint failed: user.email" in str(e.value)  # email missing
	assert User.query.filter_by(email=user['email']).count() == 0  # user does not exist


def test_create_user_username_not_unique(db, app_client):
	pass


def test_create_user_username_max_length(db, app_client):
	pass


def test_create_user_username_over_max_length(db, app_client):
	pass


def test_create_user_password_missing(db, app_client):
	pass


def test_create_user_password_max_length(db, app_client):
	pass


def test_create_user_password_over_max_length(db, app_client):
	pass


def test_create_user_first_name_missing(db, app_client):
	pass


def test_create_user_first_name_max_length(db, app_client):
	pass


def test_create_user_first_name_over_max_length(db, app_client):
	pass


def test_create_user_surname_missing(db, app_client):
	pass


def test_create_user_surname_max_length(db, app_client):
	pass


def test_create_user_surname_over_max_length(db, app_client):
	pass


def test_create_user_has_no_roles(db, app_client):
	pass


def test_create_user_has_verified_role(db, app_client):
	pass


def test_create_user_has_admin_role(db, app_client):
	pass


def test_create_user_has_admin_and_verified_roles(db, app_client):
	pass


def test_create_user_has_standard_role(db, app_client):
	pass


def test_create_user_has_standard_and_verified_roles(db, app_client):
	pass


def test_create_user_has_all_roles(db, app_client):
	pass
