from reporter_app import create_app, db
from reporter_app.models import User, Role
from sqlalchemy.sql import func
from config_testing import TestConfig
import secrets
import pytest

STANDARD_USER = User(
	username='standard',
	first_name='standard',
	surname='standard',
	email='standard@aimlackies.com',
	password='password',
	confirmed_at=func.now(),
	fs_uniquifier=secrets.token_urlsafe(64),
	active=True
)

ADMIN_USER = User(
	username='admin',
	first_name='admin',
	surname='admin',
	email='admin@aimlackies.com',
	password='password',
	confirmed_at=func.now(),
	fs_uniquifier=secrets.token_urlsafe(64),
	active=True
)


@pytest.fixture(scope='module')
def test_client():
	flask_app, user_datastore = create_app(TestConfig)

	# Create a test client using the Flask application configured for testing
	with flask_app.test_client() as testing_client:
		# Establish an application context
		with flask_app.app_context():
			yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database():
	# Create the database and the database table
	db.create_all()

	# Insert user data
	db.session.add(ADMIN_USER)
	db.session.add(STANDARD_USER)
	db.session.add(Role(
		name='admin',
		description='Manage other users on the system')
	)
	db.session.add(Role(
		name='standard',
		description='Manage the system')
	)

	# Commit the changes for the users
	db.session.commit()

	# Add roles to users (this is a bit of a hack)
	standard_user = User.query.filter_by(email=STANDARD_USER.email).first()
	admin_user = User.query.filter_by(email=ADMIN_USER.email).first()
	standard_role = Role.query.filter_by(name="standard").first()
	admin_role = Role.query.filter_by(name="admin").first()

	standard_user.roles.append(standard_role)
	admin_user.roles.append(admin_role)

	# Commit the changes for the users
	db.session.commit()

	yield db  # this is where the testing happens!

	db.drop_all()


@pytest.fixture(scope='module')
def new_admin_user():
	user = ADMIN_USER
	return user


@pytest.fixture(scope='module')
def new_standard_user():
	user = STANDARD_USER
	return user
