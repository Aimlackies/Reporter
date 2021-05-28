from reporter_app.models import Role, User
from conftest import STANDARD_USER, ADMIN_USER
from sqlalchemy.sql import func
import secrets


def login(client, email, password):
	return client.post('/login', data=dict(
		email=email,
		password=password
	), follow_redirects=True)


def create_user(db, user_dict, role_name=None, verified=True):
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

	if (role_name is not None) or verified:
		user = User.query.filter_by(email=user_dict['email']).first()
		if role_name is not None:
			role = Role.query.filter_by(name=role_name).first()
			user.roles.append(role)
		if verified:
			role = Role.query.filter_by(name="verified").first()
			user.roles.append(role)
		db.session.commit()


def get_standard_user():
	return {
		'username': 'standard',
		'first_name': 'standard',
		'surname': 'standard',
		'email': 'standard@aimlackies.com',
		'password': 'password',
		'confirmed_at': func.now(),
		'fs_uniquifier': secrets.token_urlsafe(64),
		'active': True
	}


def get_admin_user():
	return {
		'username': 'admin',
		'first_name': 'admin',
		'surname': 'admin',
		'email': 'admin@aimlackies.com',
		'password': 'password',
		'confirmed_at': func.now(),
		'fs_uniquifier': secrets.token_urlsafe(64),
		'active': True
	}
