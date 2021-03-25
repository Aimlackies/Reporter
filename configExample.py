import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://username:password@127.0.0.1/databaseName'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SUPPRESS_SEND = True

	SECRET_KEY = os.environ.get('SECRET_KEY') or '1j6EBSGw0tDHl3/Udm6i3NYMz+wrnnvUjij+ouCpPlSjXDgA7z2UW7akR9gS5ZzC9gGfiC5gMpwPsV6puKnfug=='
	SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or '291997320225856998054060676404433511338'
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
