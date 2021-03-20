from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemySessionUserDatastore, hash_password
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

# Seed database with user roles and a default admin user
@app.cli.command("seed")
def seed():
    roleAdmin = user_datastore.create_role(
        name='admin',
        description='Manage other users on the system')
    roleStandard = user_datastore.create_role(
        name='standard',
        description='Manage the system')
    userAdmin = user_datastore.create_user(
        username='admin',
        first_name='admin',
        surname='admin',
        email='admin@aimlackies.com',
        password=hash_password('password'),
        confirmed_at=func.now()
    )
    userAdmin.roles.append(roleAdmin)
    db.session.commit()

    print("done")

db.init_app(app)
