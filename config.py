import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or '1j6EBSGw0tDHl3/Udm6i3NYMz+wrnnvUjij+ouCpPlSjXDgA7z2UW7akR9gS5ZzC9gGfiC5gMpwPsV6puKnfug=='
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
