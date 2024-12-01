from flask import request, jsonify
from app import db
from app.models.category import Category
from sqlalchemy.exc import SQLAlchemyError

def create_category():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    try:
        new_category = Category(name=name, description=description)
        db.session.add(new_category)
        db.session.commit()
        return jsonify(new_category.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500

def get_categories():
    try:
        categories = Category.query.all()
        return jsonify([category.to_dict_with_subcategories() for category in categories])
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

def delete_category(category_id):
    try:
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": f"Category '{category.name}' deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def update_category(category_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    try:
        category = Category.query.get_or_404(category_id)
        if name:
            category.name = name
        if description:
            category.description = description
        db.session.commit()
        return jsonify(category.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400
