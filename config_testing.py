from config import Config


class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite://'
	WTF_CSRF_ENABLED = False
