import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	SQLALCHEMY_DATABASE_URI = os.environ.get('AIMLACKIES_REPORTER_DATABASE_URL')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SUPPRESS_SEND = True

	SECRET_KEY = os.environ.get('AIMLACKIES_REPORTER_SECRET_KEY')
	SECURITY_PASSWORD_SALT = os.environ.get('AIMLACKIES_REPORTER_SECURITY_PASSWORD_SALT')
	SECURITY_REGISTERABLE = True
	SECURITY_TRACKABLE = True
	SECURITY_MSG_INVALID_PASSWORD = ('Your username and password do not match our records', 'danger')
	SECURITY_MSG_USER_DOES_NOT_EXIST = ('Your username and password do not match our records', 'danger')
	SECURITY_MSG_PASSWORD_NOT_SET = ('Password not set', 'danger')
	SECURITY_MSG_CONFIRMATION_REQUIRED = ('Email has not been confirmed yet. Please check your emails.', 'info')
	SECURITY_MSG_DISABLED_ACCOUNT = ('This account has been disabled', 'danger')
	SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}
	SECURITY_CHANGEABLE = True
	SECURITY_RECOVERABLE = True
