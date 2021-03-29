# Setup Flask-User
user_manager = UserManager(app, db, User)

class Client(db.Model, UserMixin):
    ...

user_manager = UserManager(app, db, Client)

class User(db.Model, UserMixin):
        ...
    # Existing code uses email_address instead of email
    email_address = db.Column(db.String(255), nullable=False, unique=True)
        ...

    # define email getter
    @property
    def email(self):
        return self.email_address   # on user.email: return user.email_address

    # define email setter
    @email.setter
    def email(self, value):
        self.email_address = value  # on user.email='xyz': set user.email_address='xyz'

class User(db.Model, UserMixin):
        ...
    # Map email property to email_address column
    email = db.Column('email_address', db.String(255), nullable=False, unique=True)


# Define the User data-model
class User(db.Model, UserMixin):
        ...
    # Relationships
    roles = db.relationship('Role', secondary='user_roles')

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


admin_role = Role(name='Admin')
db.session.commit()

# Create 'user007' user with 'secret' and 'agent' roles
user1 = User(
    username='user007', email='admin@example.com', active=True,
    password=user_manager.hash_password('Password1'))
user1.roles = [admin_role,]
db.session.commit()

# Define User data-model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication fields
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    # Relationship
    user_emails = db.relationship('UserEmail')


# Define UserEmail data-model
class UserEmail(db.Model):
    __tablename__ = 'user_emails'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', uselist=False)

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    is_primary = db.Column(db.Boolean(), nullable=False, server_default='0')


# Setup Flask-User
user_manager = UserManager(app, User, UserEmailClass=UserEmail)
