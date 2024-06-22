from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_restful import Api, Resource
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import os

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://snipset_user:snipset_password@db:5432/snipset_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT', 'super-secret-salt')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)

# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all()
    if not user_datastore.find_user(email="test@example.com"):
        user_datastore.create_user(
            username="testuser",
            email="test@example.com",
            password=generate_password_hash("password"),
            name="Test",
            firstname="User"
        )
    db.session.commit()

# Define a resource for signup
class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = generate_password_hash(data['password'])
        name = data['name']
        firstname = data['firstname']
        
        try:
            user_datastore.create_user(username=username, email=email, password=password, name=name, firstname=firstname)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Username or email already exists"}), 409

        return jsonify(message="User created")

api.add_resource(Signup, '/api/signup')

# Define a resource for login
class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            return jsonify(message="Login succeeded")
        else:
            return jsonify(message="Invalid credentials"), 401

api.add_resource(Login, '/api/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
