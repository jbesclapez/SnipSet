from app import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)

    subcategories = db.relationship('Subcategory', back_populates='category')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def to_dict_with_subcategories(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'subcategories': [subcategory.to_dict() for subcategory in self.subcategories]
        }
