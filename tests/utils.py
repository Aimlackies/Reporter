from reporter_app.models import Role, User


def login(client, email, password):
	return client.post('/login', data=dict(
		email=email,
		password=password
	), follow_redirects=True)


def create_user(db, user_dict, role_name=None):
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

	if role_name is not None:
		standard_user = User.query.filter_by(email=user_dict['email']).first()
		standard_role = Role.query.filter_by(name=role_name).first()
		standard_user.roles.append(standard_role)
		db.session.commit()
