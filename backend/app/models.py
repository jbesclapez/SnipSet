from app import db
from flask_security import UserMixin
from sqlalchemy import CheckConstraint

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
    __table_args__ = (
        CheckConstraint(role.in_(['Administrator', 'Reviewer', 'End User']), name='check_role'),
    )

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)  # Added unique constraint
    description = db.Column(db.Text)

class Subcategory(db.Model):
    __tablename__ = 'subcategories'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    # Relationship with Category
    category = db.relationship('Category', backref=db.backref('subcategories', lazy=True))

class Snippet(db.Model):
    __tablename__ = 'snippets'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    subtype = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'))
    public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    language = db.Column(db.String(50), nullable=False)

    # Relationships
    category = db.relationship('Category', backref=db.backref('snippets', lazy=True))
    subcategory = db.relationship('Subcategory', backref=db.backref('snippets', lazy=True))
    user = db.relationship('User', backref=db.backref('snippets', lazy=True))

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class SnippetTag(db.Model):
    __tablename__ = 'snippet_tags'
    snippet_id = db.Column(db.Integer, db.ForeignKey('snippets.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    # Relationships
    snippet = db.relationship('Snippet', backref=db.backref('snippet_tags', cascade="all, delete-orphan"))
    tag = db.relationship('Tag', backref=db.backref('snippet_tags', cascade="all, delete-orphan"))

class Favorite(db.Model):
    __tablename__ = 'favorites'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    snippet_id = db.Column(db.Integer, db.ForeignKey('snippets.id'), primary_key=True)

    # Relationships
    user = db.relationship('User', backref=db.backref('favorites', cascade="all, delete-orphan"))
    snippet = db.relationship('Snippet', backref=db.backref('favorites', cascade="all, delete-orphan"))

class Profile(db.Model):
    __tablename__ = 'profiles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    website_url = db.Column(db.String(255))

    # Relationship
    user = db.relationship('User', backref=db.backref('profile', uselist=False, cascade="all, delete-orphan"))

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    read = db.Column(db.Boolean, default=False)

    # Relationship
    user = db.relationship('User', backref=db.backref('notifications', lazy=True, cascade="all, delete-orphan"))
