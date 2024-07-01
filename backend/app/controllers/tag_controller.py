from flask import request, jsonify
from app import db
from app.models.tag import Tag
from sqlalchemy.exc import SQLAlchemyError

def create_tag():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"error": "Tag name is required"}), 400

    try:
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        return jsonify(new_tag.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500

def get_tags():
    try:
        tags = Tag.query.all()
        return jsonify([tag.to_dict() for tag in tags])
    except SQLAlchemyError as e:
        return jsonify({"error": str(e.orig)}), 500

def update_tag(tag_id):
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"error": "Tag name is required"}), 400

    try:
        tag = Tag.query.get_or_404(tag_id)
        tag.name = name
        db.session.commit()
        return jsonify(tag.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500

def delete_tag(tag_id):
    try:
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return jsonify({"message": f"Tag '{tag.name}' deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500
