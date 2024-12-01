from flask import Blueprint, request, jsonify, session
from flask_restx import Api, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User, Role
from app import db
from flask_security import SQLAlchemyUserDatastore
from sqlalchemy.exc import SQLAlchemyError

auth_bp = Blueprint('auth', __name__)
auth_api = Api(auth_bp, version='1.0', title='Auth API', description='Authentication API', doc='/swagger/auth')

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

signup_model = auth_api.model('Signup', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'password': fields.String(required=True, description='The password'),
    'name': fields.String(required=True, description='The name'),
    'firstname': fields.String(required=True, description='The firstname')
})

login_model = auth_api.model('Login', {
    'email': fields.String(required=True, description='The email'),
    'password': fields.String(required=True, description='The password')
})

@auth_api.route('/signup')
class Signup(Resource):
    @auth_api.expect(signup_model)
    def post(self):
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']  # No need to hash here; the model handles it
        name = data['name']
        firstname = data['firstname']
        
        role_name = 'End User'
        role = user_datastore.find_role(role_name)
        if not role:
            role = user_datastore.create_role(name=role_name)

        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, 409
        if User.query.filter_by(email=email).first():
            return {"message": "Email already exists"}, 409

        try:
            new_user = user_datastore.create_user(
                username=username,
                email=email,
                password=password,
                name=name,
                firstname=firstname,
                roles=[role],
                role=role.name
            )
            db.session.add(new_user)  # Add the user to the session
            db.session.commit()
            return {"message": "User created"}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error creating user", "error": str(e)}, 500
        except Exception as e:
            return {"message": "An unexpected error occurred", "error": str(e)}, 500



@auth_api.route('/login')
class Login(Resource):
    @auth_api.expect(login_model)
    def post(self):
        data = request.get_json()
        try:
            user = User.query.filter_by(email=data['email']).first()
            if user and check_password_hash(user.password, data['password']):
                session['user_id'] = user.id
                return {"message": "Login succeeded"}, 200
            else:
                return {"message": "Invalid credentials"}, 401
        except SQLAlchemyError as e:
            return {"message": "Database error", "error": str(e)}, 500
        except Exception as e:
            return {"message": "An unexpected error occurred", "error": str(e)}, 500


@auth_api.route('/logout')
class Logout(Resource):
    def get(self):
        try:
            if 'user_id' not in session:
                return jsonify(message="User not logged in"), 400
            session.clear()
            return jsonify(message="Logout succeeded")
        except KeyError:
            return jsonify(message="User not logged in"), 400
        except Exception as e:
            return {"message": "An unexpected error occurred", "error": str(e)}, 500
