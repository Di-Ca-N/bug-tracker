from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_migrate import Migrate

db = SQLAlchemy()

def generate_id():
    return str(uuid4())

roles_users = db.Table('roles_users',
    db.Column('user_id', db.String(36), db.ForeignKey('user.id')),
    db.Column('role_id', db.String(36), db.ForeignKey('role.id')),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.String(36), primary_key=True, default=generate_id)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String())


class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=generate_id)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()
migrate = Migrate(db=db)
