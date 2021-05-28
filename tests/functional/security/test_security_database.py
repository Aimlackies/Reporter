from conftest import app_client, STANDARD_USER, ADMIN_USER, db
from utils import create_user, get_admin_user, get_standard_user
from reporter_app.models import Role, User
import pytest
from flask_security import current_user
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


@pytest.mark.parametrize("user_params, change, expect", [
	(get_standard_user(), {"drop": False, "param": "username", "value": "new_username"}, {"user_count": [1, "email"], "error_msg": None}),
	(get_standard_user(), {"drop": True, "param": "email"}, {"user_count": [0, "username"], "error_msg": "NOT NULL constraint failed: user.email"}),
	(get_standard_user(), {"drop": True, "param": "password"}, {"user_count": [0, "username"], "error_msg": "NOT NULL constraint failed: user.password"}),
	(get_standard_user(), {"drop": True, "param": "first_name"}, {"user_count": [0, "username"], "error_msg": "NOT NULL constraint failed: user.first_name"}),
	(get_standard_user(), {"drop": True, "param": "surname"}, {"user_count": [0, "username"], "error_msg": "NOT NULL constraint failed: user.surname"}),
])
def test_user_creation(db, app_client, user_params, change, expect):
	"""
	GIVEN a Flask application configured for testing and zero or one user parameters
	WHEN submitting a transaction to create a valid user
	THEN make sure the database responds as expected

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
	}
	"""
	if change["drop"]:
		del user_params[change["param"]]
	else:
		user_params[change["param"]] = change["value"]

	if expect["error_msg"] == None:
		db.session.add(User(**user_params))
	else:
		db.session.begin_nested()
		with pytest.raises(IntegrityError) as e:
			db.session.add(User(**user_params))
			db.session.commit()
		db.session.rollback()

	if expect["error_msg"] != None:
		assert expect["error_msg"] in str(e.value)
	if expect["user_count"][1] == "username":
		assert User.query.filter_by(username=user_params[expect["user_count"][1]]).count() == expect["user_count"][0]
	elif expect["user_count"][1] == "email":
		assert User.query.filter_by(email=user_params[expect["user_count"][1]]).count() == expect["user_count"][0]




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
	assert User.query.filter_by(email="email@email.com").first().username == "not_unique_user_1"  # First user that was created still exists


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
