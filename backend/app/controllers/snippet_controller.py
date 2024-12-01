from flask import request, jsonify
from app import db
from app.models.snippet import Snippet
from app.models.tag import Tag
from sqlalchemy.exc import SQLAlchemyError

def create_snippet():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    content = data.get('content')
    type = data.get('type')
    subtype = data.get('subtype')
    category_id = data.get('category_id')
    subcategory_id = data.get('subcategory_id')
    public = data.get('public', False)
    user_id = data.get('user_id')
    language = data.get('language')

    if not all([title, description, content, type, subtype, category_id, user_id, language]):
        return jsonify({"error": "All fields are required"}), 400

    try:
        new_snippet = Snippet(
            title=title,
            description=description,
            content=content,
            type=type,
            subtype=subtype,
            category_id=category_id,
            subcategory_id=subcategory_id,
            public=public,
            user_id=user_id,
            language=language
        )
        db.session.add(new_snippet)
        db.session.commit()
        return jsonify(new_snippet.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500

def get_snippets():
    try:
        snippets = Snippet.query.all()
        return jsonify([snippet.to_dict() for snippet in snippets])
    except SQLAlchemyError as e:
        return jsonify({"error": str(e.orig)}), 500

def get_snippet(snippet_id):
    try:
        snippet = Snippet.query.get_or_404(snippet_id)
        return jsonify(snippet.to_dict())
    except SQLAlchemyError as e:
        return jsonify({"error": str(e.orig)}), 500

def update_snippet(snippet_id):
    data = request.get_json()
    try:
        snippet = Snippet.query.get_or_404(snippet_id)
        snippet.title = data.get('title', snippet.title)
        snippet.description = data.get('description', snippet.description)
        snippet.content = data.get('content', snippet.content)
        snippet.type = data.get('type', snippet.type)
        snippet.subtype = data.get('subtype', snippet.subtype)
        snippet.category_id = data.get('category_id', snippet.category_id)
        snippet.subcategory_id = data.get('subcategory_id', snippet.subcategory_id)
        snippet.public = data.get('public', snippet.public)
        snippet.language = data.get('language', snippet.language)
        db.session.commit()
        return jsonify(snippet.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500

def delete_snippet(snippet_id):
    try:
        snippet = Snippet.query.get_or_404(snippet_id)
        db.session.delete(snippet)
        db.session.commit()
        return '', 204
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500

def associate_tags(snippet_id):
    data = request.get_json()
    tags = data.get('tags', [])

    try:
        snippet = Snippet.query.get_or_404(snippet_id)
        snippet.tags = []

        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            snippet.tags.append(tag)

        db.session.commit()
        return jsonify({"message": "Tags associated successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500

def get_snippets_by_tag(tag_id):
    try:
        tag = Tag.query.get_or_404(tag_id)
        snippets = [snippet.to_dict() for snippet in tag.snippets]
        return jsonify(snippets), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e.orig)}), 500
