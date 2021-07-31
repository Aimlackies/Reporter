from flask_security import hash_password
from sqlalchemy.sql import func
from reporter_app import db
from reporter_app.models import ElecUse
from reporter_app.electricity_use.utils import call_leccyfunc


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

		print("Created seed user data")

	@app.cli.command("generate_elec_use_data")
	def generate_elec_use_data():
		"""
		Grab electricity usage data and add it to electricity use DB table
		"""

		# grab elctricity usage data
		e_use_df = call_leccyfunc()

		# write elctricity usage data to database
		for idx, row in e_use_df.iterrows():
			newElecUse = ElecUse(
				date_time=row['Time'],
				electricity_use=row['Electricity Usage (kW)']
			)
			db.session.add(newElecUse)
		db.session.commit()
