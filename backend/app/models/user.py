from app import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy import CheckConstraint

# Association table for the many-to-many relationship between users and roles
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    approved = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    __table_args__ = (
        CheckConstraint(role.in_(['Administrator', 'Reviewer', 'End User']), name='check_role'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'firstname': self.firstname,
            'role': self.role,
            'created_at': self.created_at,
            'approved': self.approved,
            'active': self.active,
            'confirmed_at': self.confirmed_at
        }

class Profile(db.Model):
    __tablename__ = 'profiles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    website_url = db.Column(db.String(255))

    # Relationship
    user = db.relationship('User', backref=db.backref('profile', uselist=False, cascade="all, delete-orphan"))

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'website_url': self.website_url
        }
