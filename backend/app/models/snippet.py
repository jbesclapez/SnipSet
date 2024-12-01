from app import db

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
    tags = db.relationship('Tag', secondary='snippet_tags', backref=db.backref('snippets', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'type': self.type,
            'subtype': self.subtype,
            'category_id': self.category_id,
            'subcategory_id': self.subcategory_id,
            'public': self.public,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'language': self.language
        }

class Favorite(db.Model):
    __tablename__ = 'favorites'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    snippet_id = db.Column(db.Integer, db.ForeignKey('snippets.id'), primary_key=True)

    # Relationships
    user = db.relationship('User', backref=db.backref('favorites', cascade="all, delete-orphan"))
    snippet = db.relationship('Snippet', backref=db.backref('favorites', cascade="all, delete-orphan"))
