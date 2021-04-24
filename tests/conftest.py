from reporter_app import create_app
from reporter_app import db as _db
from reporter_app.models import Role
from sqlalchemy.sql import func
from config_testing import TestConfig
import secrets
import pytest

STANDARD_USER = {
	'username': 'standard',
	'first_name': 'standard',
	'surname': 'standard',
	'email': 'standard@aimlackies.com',
	'password': 'password',
	'confirmed_at': func.now(),
	'fs_uniquifier': secrets.token_urlsafe(64),
	'active': True
}

ADMIN_USER = {
	'username': 'admin',
	'first_name': 'admin',
	'surname': 'admin',
	'email': 'admin@aimlackies.com',
	'password': 'password',
	'confirmed_at': func.now(),
	'fs_uniquifier': secrets.token_urlsafe(64),
	'active': True
}


@pytest.fixture(scope='session')
def app(request):
	flask_app, user_datastore = create_app(TestConfig)

	with flask_app.test_client() as client:
		with flask_app.app_context():
			yield client


@pytest.fixture(scope='session')
def create_db_with_sqlalchemy(app, request):
	# bind the app the database instance
	_db.app = app

	_db.create_all()

	def teardown():
		_db.session.remove()
		_db.drop_all()

	request.addfinalizer(teardown)

	return _db


@pytest.fixture
def db(create_db_with_sqlalchemy, request):
	db = create_db_with_sqlalchemy

	def cleanup_tables():
		# sort tables with topology order, ensure children tables are
		# deleted first
		for table in db.metadata.sorted_tables[::-1]:
			db.session.execute(table.delete())
		db.session.commit()

	cleanup_tables()
	request.addfinalizer(cleanup_tables)

	db.session.add(Role(
		name='admin',
		description='Manage other users on the system')
	)
	db.session.add(Role(
		name='standard',
		description='Manage the system')
	)
	db.session.add(Role(
		name='verified',
		description='User has been verified and can use the system')
	)

	# Commit the changes for the users
	db.session.commit()

	return db


@pytest.fixture
def app_client(db, app):
	"""Create api request client."""
	return app
