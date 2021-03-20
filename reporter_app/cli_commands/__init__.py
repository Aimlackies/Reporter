from flask import Blueprint
from reporter_app import db
import reporter_app.models

bp = Blueprint('cli_commands', __name__)


# Seed database with user roles and a default admin user
@bp.cli.command("seed")
def seed():
    user_datastore = SQLAlchemySessionUserDatastore(db.session, reporter_app.models.User, reporter_app.models.Role)

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
