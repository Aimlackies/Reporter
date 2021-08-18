from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemySessionUserDatastore
from sassutils.wsgi import SassMiddleware
from flask_mail import Mail
from reporter_app.utils import seed as seed_db

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
security = Security()


import reporter_app.models
import reporter_app.forms


def create_app(config_class=Config):
    """
    Construct Flash application without a global variable. This make it easier
    to run unit tests
    """
    app = Flask(__name__)
    # Add SCSS to CSS while in development
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'reporter_app': ('static/scss', 'static/css', '/static/css')
    })
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    user_datastore = SQLAlchemySessionUserDatastore(db.session, reporter_app.models.User, reporter_app.models.Role)
    security = Security(
        app,
        user_datastore,
        register_form=reporter_app.forms.ExtendedRegisterForm,
        login_form=reporter_app.forms.ExtendedLoginForm
    )
    mail.init_app(app)

    # Dashboard
    from reporter_app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    # Error pages and functions
    from reporter_app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # User pages
    from reporter_app.users import bp as users_bp
    app.register_blueprint(users_bp)

    # Building electricity usage data page
    from reporter_app.electricity_use import bp as electricity_use_bp
    app.register_blueprint(electricity_use_bp)

    # Site electricity generation data page
    from reporter_app.electricity_gen import bp as electricity_gen_bp
    app.register_blueprint(electricity_gen_bp)

    # Site net power usage data
    from reporter_app.net_power import bp as net_power_bp
    app.register_blueprint(net_power_bp)

    # CO2 savings
    from reporter_app.co2 import bp as co2_bp
    app.register_blueprint(co2_bp)

    # Normal app startup
    if not app.debug and not app.testing:
        pass

    return app, user_datastore
