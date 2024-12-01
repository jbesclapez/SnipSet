from flask import request, jsonify
from app import db
from app.models.user import User, Profile
from sqlalchemy.exc import SQLAlchemyError

def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    firstname = data.get('firstname')
    role = data.get('role')

    if not all([username, email, password, name, firstname, role]):
        return jsonify({"error": "All fields are required"}), 400

    try:
        new_user = User(
            username=username,
            email=email,
            password=password,
            name=name,
            firstname=firstname,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()

        # Create a profile for the new user
        new_profile = Profile(user_id=new_user.id)
        db.session.add(new_profile)
        db.session.commit()

        return jsonify(new_user.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500

def get_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    except SQLAlchemyError as e:
        return jsonify({"error": str(e.orig)}), 500

def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())
    except SQLAlchemyError as e:
        return jsonify({"error": str(e.orig)}), 500

def update_user(user_id):
    data = request.get_json()
    try:
        user = User.query.get_or_404(user_id)
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = data['password']
        if 'name' in data:
            user.name = data['name']
        if 'firstname' in data:
            user.firstname = data['firstname']
        if 'role' in data:
            user.role = data['role']
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User '{user.username}' deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_user_profile(user_id):
    try:
        profile = Profile.query.filter_by(user_id=user_id).first()
        if profile:
            return jsonify(profile.to_dict())
        else:
            return jsonify({"error": "Profile not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": str(e.orig)}), 500

def update_user_profile(user_id):
    data = request.get_json()
    try:
        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            return jsonify({"error": "Profile not found"}), 404
        if 'bio' in data:
            profile.bio = data['bio']
        if 'avatar_url' in data:
            profile.avatar_url = data['avatar_url']
        if 'website_url' in data:
            profile.website_url = data['website_url']
        db.session.commit()
        return jsonify(profile.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400
