from flask import request, jsonify
from app import db
from app.models.subcategory import Subcategory
from sqlalchemy.exc import SQLAlchemyError

def create_subcategory():
    data = request.get_json()
    category_id = data.get('category_id')
    name = data.get('name')
    description = data.get('description')

    if not category_id or not name:
        return jsonify({"error": "Category ID and Name are required"}), 400

    try:
        new_subcategory = Subcategory(category_id=category_id, name=name, description=description)
        db.session.add(new_subcategory)
        db.session.commit()
        return jsonify(new_subcategory.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_subcategories():
    try:
        subcategories = Subcategory.query.all()
        return jsonify([subcategory.to_dict() for subcategory in subcategories])
    except SQLAlchemyError as e:
        return jsonify({"error": str(e.orig)}), 500

def delete_subcategory(subcategory_id):
    try:
        subcategory = Subcategory.query.get_or_404(subcategory_id)
        db.session.delete(subcategory)
        db.session.commit()
        return jsonify({"message": f"Subcategory '{subcategory.name}' deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_subcategories_by_category(category_id):
    try:
        subcategories = Subcategory.query.filter_by(category_id=category_id).all()
        return jsonify([subcategory.to_dict() for subcategory in subcategories])
    except SQLAlchemyError as e:
        return jsonify({"error": str(e.orig)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_subcategory(subcategory_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    try:
        subcategory = Subcategory.query.get_or_404(subcategory_id)
        if name:
            subcategory.name = name
        if description:
            subcategory.description = description
        db.session.commit()
        return jsonify(subcategory.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400
