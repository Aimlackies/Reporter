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
    name = Column(String(80), unique=True)
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
