from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemySessionUserDatastore
from sassutils.wsgi import SassMiddleware
from flask_mail import Mail
from reporter_app.utils import seed as seed_db

app = Flask(__name__)
# Add SCSS to CSS while in development
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'reporter_app': ('static/scss', 'static/css', '/static/css')
})
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Dashboard
from reporter_app.dashboard import bp as dashboard_bp
app.register_blueprint(dashboard_bp)

# Error pages and functions
from reporter_app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

# User pages
from reporter_app.users import bp as users_bp
app.register_blueprint(users_bp)

import reporter_app.models
import reporter_app.forms

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db.session, reporter_app.models.User, reporter_app.models.Role)
security = Security(
    app,
    user_datastore,
    register_form=reporter_app.forms.ExtendedRegisterForm,
    login_form=reporter_app.forms.ExtendedLoginForm
)


@app.cli.command("seed")
def seed():
    seed_db(user_datastore, db)


db.init_app(app)
