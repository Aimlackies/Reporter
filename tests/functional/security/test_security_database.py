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
	THEN check the transaction has been a success and the user is in the DB
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
	assert len(User.query.filter_by(username=STANDARD_USER['username']).first().roles) == 0  # New user has no roles


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
	assert User.query.filter_by(email="email@email.com").count() == 1  # Only one uesr exists
	assert User.query.filter_by(email="email@email.com").first().username == "not_unique_user_1" # First user that was created still exists


def test_create_user_username_not_unique(db, app_client):
	"""
	GIVEN a Flask application configured for testing and a user already created
	WHEN submitting a transaction to create a user after a user with the same usename exists
	THEN check the transaction has been a unsuccessful for the username parameter and the user is not in the DB
	"""

	not_unique_user_1 = get_standard_user()
	not_unique_user_1["username"] = "not_unique_user"
	not_unique_user_1["email"] = "email@email.com"
	not_unique_user_2 = get_standard_user()
	not_unique_user_2["username"] = "not_unique_user"
	not_unique_user_2["email"] = "email2@email.com"

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

	assert "UNIQUE constraint failed: user.username" in str(e.value)  # username not unique
	assert User.query.filter_by(email="email@email.com").count() == 1  # Only one uesr exists
	assert User.query.filter_by(email="email2@email.com").count() == 0  # no uesrs exists
	assert User.query.filter_by(email="email@email.com").first().username == "not_unique_user" # First user that was created still exists


def test_create_user_password_missing(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a user without a password
	THEN check the transaction has been a unsuccessful for the password parameter and the user is not in the DB
	"""

	user = get_standard_user()

	db.session.begin_nested()
	with pytest.raises(IntegrityError) as e:
		db.session.add(User(
			username="user_missing_password",
			first_name=user['first_name'],
			surname=user['surname'],
			email=user['email'],
			confirmed_at=user['confirmed_at'],
			fs_uniquifier=user['fs_uniquifier'],
			active=user['active']
		))

		db.session.commit()
	db.session.rollback()

	assert "NOT NULL constraint failed: user.password" in str(e.value)  # email missing
	assert User.query.filter_by(username="user_missing_password").count() == 0  # user does not exist


def test_create_user_first_name_missing(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a user without a first name
	THEN check the transaction has been a unsuccessful for the first_name parameter and the user is not in the DB
	"""

	user = get_standard_user()

	db.session.begin_nested()
	with pytest.raises(IntegrityError) as e:
		db.session.add(User(
			username="user_missing_first_name",
			surname=user['surname'],
			email=user['email'],
			password=user['password'],
			confirmed_at=user['confirmed_at'],
			fs_uniquifier=user['fs_uniquifier'],
			active=user['active']
		))

		db.session.commit()
	db.session.rollback()

	assert "NOT NULL constraint failed: user.first_name" in str(e.value)  # email missing
	assert User.query.filter_by(username="user_missing_first_name").count() == 0  # user does not exist


def test_create_user_surname_missing(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a user without a surname
	THEN check the transaction has been a unsuccessful for the surname parameter and the user is not in the DB
	"""

	user = get_standard_user()

	db.session.begin_nested()
	with pytest.raises(IntegrityError) as e:
		db.session.add(User(
			username="user_missing_surname",
			first_name=user['first_name'],
			email=user['email'],
			password=user['password'],
			confirmed_at=user['confirmed_at'],
			fs_uniquifier=user['fs_uniquifier'],
			active=user['active']
		))

		db.session.commit()
	db.session.rollback()

	assert "NOT NULL constraint failed: user.surname" in str(e.value)  # email missing
	assert User.query.filter_by(username="user_missing_surname").count() == 0  # user does not exist


def test_create_user_has_verified_role(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a valid user and adding verified role
	THEN check the transaction has been a success and the user is in the DB with the role verified
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

	new_user = User.query.filter_by(username=STANDARD_USER['username']).first()
	verified_role = Role.query.filter_by(name='verified').first()
	new_user.roles.append(verified_role)
	db.session.commit()

	assert User.query.filter_by(username=STANDARD_USER['username']).count() == 1  # user does not exist
	assert len(User.query.filter_by(username=STANDARD_USER['username']).first().roles) == 1  # verified is a role and the only one the user has
	assert User.query.filter_by(username=STANDARD_USER['username']).first().has_role('verified') == True  # user has verified role


def test_create_user_has_admin_role(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a valid user and adding admin role
	THEN check the transaction has been a success and the user is in the DB with the role admin
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

	new_user = User.query.filter_by(username=STANDARD_USER['username']).first()
	admin_role = Role.query.filter_by(name='admin').first()
	new_user.roles.append(admin_role)
	db.session.commit()

	assert User.query.filter_by(username=STANDARD_USER['username']).count() == 1  # user does not exist
	assert len(User.query.filter_by(username=STANDARD_USER['username']).first().roles) == 1  # admin is a role and the only one the user has
	assert User.query.filter_by(username=STANDARD_USER['username']).first().has_role('admin') == True  # user has admin role


def test_create_user_has_admin_and_verified_roles(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a valid user and adding admin and verified role
	THEN check the transaction has been a success and the user is in the DB with the role admin and verified
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

	new_user = User.query.filter_by(username=STANDARD_USER['username']).first()
	verified_role = Role.query.filter_by(name='verified').first()
	admin_role = Role.query.filter_by(name='admin').first()
	new_user.roles.append(verified_role)
	new_user.roles.append(admin_role)
	db.session.commit()

	assert User.query.filter_by(username=STANDARD_USER['username']).count() == 1  # user does not exist
	assert len(User.query.filter_by(username=STANDARD_USER['username']).first().roles) == 2  # user has 2 roles
	assert User.query.filter_by(username=STANDARD_USER['username']).first().has_role('admin') == True  # user has admin role
	assert User.query.filter_by(username=STANDARD_USER['username']).first().has_role('verified') == True  # user has verified role


def test_create_user_has_standard_role(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a valid user and adding standard role
	THEN check the transaction has been a success and the user is in the DB with the role standard
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

	new_user = User.query.filter_by(username=STANDARD_USER['username']).first()
	standard_role = Role.query.filter_by(name='standard').first()
	new_user.roles.append(standard_role)
	db.session.commit()

	assert User.query.filter_by(username=STANDARD_USER['username']).count() == 1  # user does not exist
	assert len(User.query.filter_by(username=STANDARD_USER['username']).first().roles) == 1  # standard is a role and the only one the user has
	assert User.query.filter_by(username=STANDARD_USER['username']).first().has_role('standard') == True  # user has standard role


def test_create_user_has_standard_and_verified_roles(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a valid user and adding standard and verified role
	THEN check the transaction has been a success and the user is in the DB with the role standard and verified
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

	new_user = User.query.filter_by(username=STANDARD_USER['username']).first()
	verified_role = Role.query.filter_by(name='verified').first()
	standard_role = Role.query.filter_by(name='standard').first()
	new_user.roles.append(verified_role)
	new_user.roles.append(standard_role)
	db.session.commit()

	assert User.query.filter_by(username=STANDARD_USER['username']).count() == 1  # user does not exist
	assert len(User.query.filter_by(username=STANDARD_USER['username']).first().roles) == 2  # user has 2 roles
	assert User.query.filter_by(username=STANDARD_USER['username']).first().has_role('standard') == True  # user has standard role
	assert User.query.filter_by(username=STANDARD_USER['username']).first().has_role('verified') == True  # user has verified role


def test_create_user_has_all_roles(db, app_client):
	"""
	GIVEN a Flask application configured for testing
	WHEN submitting a transaction to create a valid user and adding all roles
	THEN check the transaction has been a success and the user is in the DB with all roles
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

	new_user = User.query.filter_by(username=STANDARD_USER['username']).first()
	verified_role = Role.query.filter_by(name='verified').first()
	standard_role = Role.query.filter_by(name='standard').first()
	admin_role = Role.query.filter_by(name='admin').first()
	new_user.roles.append(verified_role)
	new_user.roles.append(standard_role)
	new_user.roles.append(admin_role)
	db.session.commit()

	assert User.query.filter_by(username=STANDARD_USER['username']).count() == 1  # user does not exist
	assert len(User.query.filter_by(username=STANDARD_USER['username']).first().roles) == 3  # user has 2 roles
	assert User.query.filter_by(username=STANDARD_USER['username']).first().has_role('standard') == True  # user has standard role
	assert User.query.filter_by(username=STANDARD_USER['username']).first().has_role('verified') == True  # user has verified role
	assert User.query.filter_by(username=STANDARD_USER['username']).first().has_role('admin') == True  # user has verified role
