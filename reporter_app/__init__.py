from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemySessionUserDatastore
from sassutils.wsgi import SassMiddleware
from flask_mail import Mail

app = Flask(__name__)
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'reporter_app': ('static/scss', 'static/css', '/static/css')
})
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

import reporter_app.routes
import reporter_app.models
import reporter_app.errors
import reporter_app.forms

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db.session, reporter_app.models.User, reporter_app.models.Role)
security = Security(
    app,
    user_datastore,
    register_form=reporter_app.forms.ExtendedRegisterForm,
    login_form=reporter_app.forms.ExtendedLoginForm
)

db.init_app(app)
