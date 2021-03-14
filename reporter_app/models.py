from reporter_app import db
from flask_login import UserMixin
from reporter_app import login
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(32), default="user", nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
