from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sassutils.wsgi import SassMiddleware

app = Flask(__name__)
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'reporter_app': ('static/scss', 'static/css', '/static/css')
})
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

import reporter_app.routes
import reporter_app.models
import reporter_app.errors

db.init_app(app)
