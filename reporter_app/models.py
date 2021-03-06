from reporter_app import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, UnicodeText, UniqueConstraint
from sqlalchemy.sql import func
import datetime


class RolesUsers(db.Model):
	__tablename__ = 'roles_users'
	__table_args__ = (UniqueConstraint('user_id', 'role_id'),)
	user_id = Column('user_id', Integer(), ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
	role_id = Column('role_id', Integer(), ForeignKey('role.id', ondelete='CASCADE'), primary_key=True)
	create_datetime = Column(DateTime(), nullable=False, server_default=func.now())
	update_datetime = Column(
		DateTime(),
		nullable=False,
		server_default=func.now(),
		onupdate=datetime.datetime.utcnow,
	)


class Role(db.Model, RoleMixin):
	__tablename__ = 'role'
	id = Column(Integer(), primary_key=True)
	name = Column(String(80), unique=True, nullable=False)
	description = Column(String(255))
	create_datetime = Column(DateTime(), nullable=False, server_default=func.now())
	update_datetime = Column(
		DateTime(),
		nullable=False,
		server_default=func.now(),
		onupdate=datetime.datetime.utcnow,
	)


class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	email = Column(String(255), unique=True, nullable=False)
	username = Column(String(255), unique=True, nullable=True)
	password = Column(String(255), nullable=False)
	first_name = Column(String(128), nullable=False)
	surname = Column(String(128), nullable=False)
	last_login_at = Column(DateTime())
	current_login_at = Column(DateTime())
	last_login_ip = Column(String(100))
	current_login_ip = Column(String(100))
	login_count = Column(Integer)
	active = Column(Boolean())
	fs_uniquifier = Column(String(255), unique=True, nullable=False)
	confirmed_at = Column(DateTime())
	roles = relationship('Role', secondary='roles_users',
	                     backref=backref('users', lazy='dynamic'))
	create_datetime = Column(DateTime(), nullable=False, server_default=func.now())
	update_datetime = Column(
		DateTime(),
		nullable=False,
		server_default=func.now(),
		onupdate=datetime.datetime.utcnow,
	)

	def has_role(self, role):
		return role in self.roles


class Co2(db.Model):
	__tablename__ = 'co2'
	date_time = Column(DateTime(), ForeignKey('elec_use.date_time', ondelete='CASCADE'), primary_key=True)
	co2 = Column(db.Float)
	usage = relationship('ElecUse', backref=backref('co2', lazy='dynamic'))


class ElecUse(db.Model):
	_tablename__ = 'electricity_use'
	date_time = Column(DateTime(), primary_key=True)
	electricity_use = Column(db.Float)


class RealPowerReadings(db.Model):
	__tablename__ = 'real_power_readings'
	__table_args__ = (UniqueConstraint('date_time', 'device_name'),)
	date_time = Column(DateTime(), primary_key=True)
	device_name = Column(String(255), primary_key=True)
	power = Column(db.Float)
	power_generator = Column(Boolean())
	create_datetime = Column(DateTime(), nullable=False, server_default=func.now())
	update_datetime = Column(
		DateTime(),
		nullable=False,
		server_default=func.now(),
		onupdate=datetime.datetime.utcnow,
	)


class RealSiteReadings(db.Model):
	__tablename__ = 'real_site_readings'
	date_time = Column(DateTime(), primary_key=True)
	temperature = Column(db.Float)
	power = Column(db.Float)
	create_datetime = Column(DateTime(), nullable=False, server_default=func.now())
	update_datetime = Column(
		DateTime(),
		nullable=False,
		server_default=func.now(),
		onupdate=datetime.datetime.utcnow,
	)

class Trading(db.Model):
    __tablename__='trading'
    __table_args__ = (UniqueConstraint('date_time', 'Period'),)    
    date_time=Column("date_time" , DateTime(), primary_key=True)
    period=Column("Period",Integer(), primary_key=True,nullable=False)
    bid_units=Column("Bid Units Volume(kWh)",db.Float)
    bid_type=Column("Bid type",String(255))
    bid_price=Column("Bid Price",db.Float)
    bid_outcome=Column("Bid outcome",db.Float)

    
class ClearoutPrice(db.Model):
    __tablename__='clearout_price'        
    date_time=Column("date_time" , DateTime(), primary_key=True)
    period=Column("Period",Integer(), primary_key=True,nullable=False)    
    closing_price=Column("Bid closing price",db.Float)
    volume=Column("Volume", db.Float)
    


class PredictedPrice(db.Model):
    __tablename__='predicted_price'
    date_time=Column("Date, time" , DateTime(),unique=True, primary_key=True)
    period=Column("Period",Integer(),nullable=False)
    predicted_load=Column("Predicted grid load(MWh)",db.Float,nullable=False)
    predicted_price=Column("Predicted market price",db.Float, nullable=False)

class ActualLoad(db.Model):
    __tablename__='actual_load'
    date_time=Column("Date, time" , DateTime(),unique=True, primary_key=True)
    period=Column("Period",Integer(),nullable=False)
    actual_generation=Column("Volume Generated onsite",db.Float)
    actual_usage=Column("Volume consumed onsite",db.Float)
    imbalance_vol=Column("Imbalance volume",db.Float)
    imbalance_price=Column("Imbalance Price",db.Float)
    net_profit=Column("Net profit",db.Float)


class ElecGen(db.Model):
	_tablename__ = 'electricity_gen'
	date_time = Column(DateTime(), primary_key=True)
	wind_gen = Column(db.Float)
	solar_gen = Column(db.Float)
