import logging
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://snipset_user:snipset_password@db:5432/snipset_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT', 'super-secret-salt')
app.config['RECAPTCHA_SECRET_KEY'] = os.getenv('RECAPTCHA_SECRET_KEY', '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app, version='1.0', title='SnipSet API', description='A simple API for SnipSet', doc='/swagger/')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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

    # Get default admin credentials from environment variables
    default_admin_email = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@example.com')
    default_admin_password = os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin_password')

    # Check if the default admin role exists, create it if it doesn't
    if not user_datastore.find_role('Administrator'):
        user_datastore.create_role(name='Administrator', description='Administrator role')
    
    # Check if the default admin user exists, create it if it doesn't
    if not user_datastore.find_user(email=default_admin_email):
        user_datastore.create_user(
            username='admin',
            email=default_admin_email,
            password=generate_password_hash(default_admin_password),
            name='Admin',
            firstname='User',
            roles=['Administrator']
        )
    db.session.commit()

# Define API models for documentation
signup_model = api.model('Signup', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'password': fields.String(required=True, description='The password'),
    'name': fields.String(required=True, description='The name'),
    'firstname': fields.String(required=True, description='The firstname')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='The email'),
    'password': fields.String(required=True, description='The password')
})

query_model = api.model('Query', {
    'query': fields.String(required=True, description='The SQL query')
})

# Define a resource for signup
@api.route('/api/signup')
class Signup(Resource):
    @api.expect(signup_model)
    def post(self):
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = generate_password_hash(data['password'])
        name = data['name']
        firstname = data['firstname']
        user_datastore.create_user(username=username, email=email, password=password, name=name, firstname=firstname)
        db.session.commit()
        return jsonify(message="User created")

# Define a resource for login
@api.route('/api/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.get_json()
        recaptcha_token = data.get('recaptchaToken')
        recaptcha_secret = app.config['RECAPTCHA_SECRET_KEY']

#        recaptcha_response = requests.post(
#            'https://www.google.com/recaptcha/api/siteverify',
#            data={'secret': recaptcha_secret, 'response': recaptcha_token}
#        )

        recaptcha_result = recaptcha_response.json()
        if not recaptcha_result.get('success'):
            return jsonify(message="reCAPTCHA verification failed"), 400

        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            return jsonify(message="Login succeeded")
        else:
            return jsonify(message="Invalid credentials"), 401

# Define a resource for executing queries
@api.route('/api/execute_query')
class ExecuteQuery(Resource):
    @api.expect(query_model)
    def post(self):
        data = request.get_json()
        query = data.get('query')

        if not query.lower().startswith('select'):
            return jsonify({"message": "Only SELECT queries are allowed"}), 400

        try:
            logging.debug(f"Executing query: {query}")
            result = db.session.execute(query)
            rows = [dict(row) for row in result.mappings()]
            logging.debug(f"Query result: {rows}")
            return jsonify(rows)
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0')
