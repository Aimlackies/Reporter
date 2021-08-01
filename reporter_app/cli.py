from flask_security import hash_password
from sqlalchemy.sql import func
from reporter_app import db
from reporter_app.models import ElecUse, Co2
from reporter_app.electricity_use.utils import call_leccyfunc

from datetime import datetime, timedelta
import json
import requests


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

	@app.cli.command("co2_for_time")
	def co2ForTime():
		'''
		Looks up CO2 intensity from api.carbonintensity.org and writes to the database
		'''
		#rounds the current time down to nearest 30 minutes (to allow for database relationship with electricity usage
		now = datetime.now()
		start = now - (now - datetime.min) % timedelta(minutes=30)

		print("start:", start)

		#Get date and format it for url
		end = start + timedelta(minutes=30) #api requires an end time as well, so add 30 minutes to the start time
		url=("https://api.carbonintensity.org.uk/regional/intensity/" + str(start.strftime("%Y-%m-%dT%H:%MZ")) + "/" + str(end.strftime("%Y-%m-%dT%H:%MZ")) + "/regionid/7")
		#print(url)

		#Fetch data from from API
		response = requests.get(url)

		#select co2 forecast from within json data
		data = response.json()
		co2Forecast = data["data"]["data"][0]["intensity"]["forecast"]

		newCo2Value = Co2(
			date_time=start,
			co2=co2Forecast
		)

		db.session.add(newCo2Value)
		db.session.commit()

		print ("For the 30-min time period starting:", start, "the grid CO2 intensity (gCO2/kWh) was:", co2Forecast)
