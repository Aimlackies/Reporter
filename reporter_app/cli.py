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

	@app.cli.command("seed_dummy_data")
	def seed_dummy_data():
		"""
		Seed database with dummy data for testing. This should not be run on production
		"""

		# grab elctricity usage data end elec gen data.
		e_use_df = call_leccyfunc()
		e_gen_df = get_energy_gen()

		# write elctricity usage data to database
		for idx, row in e_use_df.iterrows():
			newElecUse = ElecUse(
				date_time=row['Time'],
				electricity_use=row['Electricity Usage (kW)']
			)
			db.session.add(newElecUse)
		db.session.commit()

		# write elctricity gen data to database
		numOfTurbunes = 4 #2 Originals plus 2 extra Ed mentioned...?
		for idx, row in e_gen_df['windenergy'].iterrows():
			newElecGen = ElecGen(
				date_time=row['Time'],
				electricity_gen=row['windenergy'] * numOfTurbunes
				device = "Wind"
			)
			db.session.add(newElecGen)
		db.session.commit()

		metresSquaredOfSolarPanels = 43.75 #This seems like quite a lot but apparently we have 1400 a5 panels so yea... ~44sqm 
		for idx, row in e_gen_df['totalSolarEnergy'].iterrows():
			newElecGen = ElecGen(
				date_time=row['Time'],
				electricity_gen=row['totalSolarEnergy'] * metresSquaredOfSolarPanels
				device = "Solar"
			)
			db.session.add(newElecGen)
		db.session.commit()



		print("Seeded database with dummy data")
