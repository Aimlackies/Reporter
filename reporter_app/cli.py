from flask_security import hash_password
from sqlalchemy.sql import func
from reporter_app import db


def register(app, user_datastore):
    @app.cli.command("seed")
    def seed():
        """
        Seed database with all roles and an admin user
        """
        roleAdmin = user_datastore.create_role(
            name='admin',
            description='Manage other users on the system')
        roleStandard = user_datastore.create_role(
            name='standard',
            description='Manage the system')
        roleVerified = user_datastore.create_role(
            name='verified',
            description='User has been verified and can use the system')
        userAdmin = user_datastore.create_user(
            username='admin',
            first_name='admin',
            surname='admin',
            email='admin@aimlackies.com',
            password=hash_password('password'),
            confirmed_at=func.now()
        )
        userAdmin.roles.append(roleAdmin)
        userAdmin.roles.append(roleVerified)
        db.session.commit()
