from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Snippet
from app.controllers.auth_controller import auth_bp
from app.controllers.category_controller import create_category, get_categories, delete_category, update_category
from app.controllers.subcategory_controller import create_subcategory, get_subcategories, delete_subcategory, get_subcategories_by_category, update_subcategory
from app.controllers.user_controller import create_user, get_users, get_user, update_user, delete_user, get_user_profile, update_user_profile
from app.controllers.tag_controller import create_tag, get_tags, update_tag, delete_tag
from app.controllers.snippet_controller import create_snippet, get_snippets, get_snippet, update_snippet, delete_snippet, associate_tags, get_snippets_by_tag
from app.controllers.query_controller import query_bp

api = Blueprint('api', __name__)

# Register the authentication blueprint
api.register_blueprint(auth_bp, url_prefix='/auth')

@api.route('/signup', methods=['POST'])
def signup():
    return auth_api.resources['Signup'].dispatch_request()

@api.route('/logout', methods=['GET'])
def logout():
    return auth_api.resources['Logout'].dispatch_request()

@api.route('/change_password', methods=['POST'])
def change_password():
    return auth_api.resources['ChangePassword'].dispatch_request()

@api.route('/snippets', methods=['GET'])
def get_snippets():
    snippets = Snippet.query.all()
    return jsonify([snippet.to_dict() for snippet in snippets])

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

# Add the new category routes
@api.route('/categories', methods=['POST'])
def create_category_route():
    return create_category()

@api.route('/categories', methods=['GET'])
def get_categories_route():
    return get_categories()

@api.route('/categories/<int:category_id>', methods=['PUT'])
def update_category_route(category_id):
    return update_category(category_id)

@api.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category_route(category_id):
    return delete_category(category_id)

# Add the new subcategory routes
@api.route('/subcategories', methods=['POST'])
def create_subcategory_route():
    return create_subcategory()

@api.route('/subcategories/<int:subcategory_id>', methods=['PUT'])
def update_subcategory_route(subcategory_id):
    return update_subcategory(subcategory_id)

@api.route('/subcategories/<int:subcategory_id>', methods=['DELETE'])
def delete_subcategory_route(subcategory_id):
    return delete_subcategory(subcategory_id)

@api.route('/subcategories', methods=['GET'])
def get_subcategories_route():
    return get_subcategories()

@api.route('/categories/<int:category_id>/subcategories', methods=['GET'])
def get_subcategories_by_category_route(category_id):
    return get_subcategories_by_category(category_id)

# Add the new user routes
@api.route('/users', methods=['POST'])
def create_user_route():
    return create_user()

@api.route('/users', methods=['GET'])
def get_users_route():
    return get_users()

@api.route('/users/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    return get_user(user_id)

@api.route('/users/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    return update_user(user_id)

@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    return delete_user(user_id)

@api.route('/users/<int:user_id>/profile', methods=['GET'])
def get_user_profile_route(user_id):
    return get_user_profile(user_id)

@api.route('/users/<int:user_id>/profile', methods=['PUT'])
def update_user_profile_route(user_id):
    return update_user_profile(user_id)

# Add the new tag routes
@api.route('/tags', methods=['POST'])
def create_tag_route():
    return create_tag()

@api.route('/tags', methods=['GET'])
def get_tags_route():
    return get_tags()

@api.route('/tags/<int:tag_id>', methods=['PUT'])
def update_tag_route(tag_id):
    return update_tag(tag_id)

@api.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag_route(tag_id):
    return delete_tag(tag_id)

@api.route('/tags/<int:tag_id>/snippets', methods=['GET'])
def get_snippets_by_tag_route(tag_id):
    return get_snippets_by_tag(tag_id)


# Snippet routes
@api.route('/snippets', methods=['POST'])
def create_snippet_route():
    return create_snippet()

@api.route('/snippets', methods=['GET'])
def get_snippets_route():
    return get_snippets()

@api.route('/snippets/<int:snippet_id>', methods=['GET'])
def get_snippet_route(snippet_id):
    return get_snippet(snippet_id)

@api.route('/snippets/<int:snippet_id>', methods=['PUT'])
def update_snippet_route(snippet_id):
    return update_snippet(snippet_id)

@api.route('/snippets/<int:snippet_id>', methods=['DELETE'])
def delete_snippet_route(snippet_id):
    return delete_snippet(snippet_id)

@api.route('/snippets/<int:snippet_id>/tags', methods=['POST'])
def associate_tags_route(snippet_id):
    return associate_tags(snippet_id)

# Register the query blueprint
api.register_blueprint(query_bp, url_prefix='/api/query')