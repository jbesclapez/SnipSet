from app import db

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class SnippetTag(db.Model):
    __tablename__ = 'snippet_tags'
    snippet_id = db.Column(db.Integer, db.ForeignKey('snippets.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    # Relationships
    snippet = db.relationship('Snippet', backref=db.backref('snippet_tags', cascade="all, delete-orphan"))
    tag = db.relationship('Tag', backref=db.backref('snippet_tags', cascade="all, delete-orphan"))
