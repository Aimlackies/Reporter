from config import Config


class TestConfig(Config):
	TESTING = True
	SESSION_TYPE = 'filesystem'
	SQLALCHEMY_DATABASE_URI = 'sqlite://'
