from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Snippet

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login():
    # Implement login logic here
    pass

@api.route('/signup', methods=['POST'])
def signup():
    # Implement signup logic here
    pass

@api.route('/logout', methods=['GET'])
def logout():
    # Implement logout logic here
    pass

@api.route('/snippets', methods=['GET'])
def get_snippets():
    snippets = Snippet.query.all()
    return jsonify([snippet.to_dict() for snippet in snippets])

@api.route('/snippets', methods=['POST'])
def create_snippet():
    data = request.json
    snippet = Snippet(**data)
    db.session.add(snippet)
    db.session.commit()
    return jsonify(snippet.to_dict()), 201

@api.route('/snippets/<int:id>', methods=['GET'])
def get_snippet(id):
    snippet = Snippet.query.get_or_404(id)
    return jsonify(snippet.to_dict())

@api.route('/snippets/<int:id>', methods=['PUT'])
def update_snippet(id):
    data = request.json
    snippet = Snippet.query.get_or_404(id)
    for key, value in data.items():
        setattr(snippet, key, value)
    db.session.commit()
    return jsonify(snippet.to_dict())

@api.route('/snippets/<int:id>', methods=['DELETE'])
def delete_snippet(id):
    snippet = Snippet.query.get_or_404(id)
    db.session.delete(snippet)
    db.session.commit()
    return '', 204
