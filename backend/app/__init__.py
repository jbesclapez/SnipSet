from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash
import os

db = SQLAlchemy()
migrate = Migrate()
security = Security()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://snipset_user:snipset_password@db:5432/snipset_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret')
    app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT', 'super-secret-salt')

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    with app.app_context():
        from .models.user import User, Profile, Role
        from .models.category import Category
        from .models.subcategory import Subcategory
        from .models.snippet import Snippet, Favorite
        from .models.tag import Tag, SnippetTag
        from .models.notification import Notification

        # Setup Flask-Security
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security.init_app(app, user_datastore)

        # Create a user to test with
        @app.before_first_request
        def create_user():
            db.create_all()

            # Get default admin credentials from environment variables
            default_admin_email = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@example.com')
            default_admin_password = os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin_password')

            # Check if the default admin role exists, create it if it doesn't
            if not user_datastore.find_role('Administrator'):
                admin_role = user_datastore.create_role(name='Administrator', description='Administrator role')
            else:
                admin_role = user_datastore.find_role('Administrator')

            # Check if the default admin user exists, create it if it doesn't
            if not user_datastore.find_user(email=default_admin_email):
                user_datastore.create_user(
                    username='admin',
                    email=default_admin_email,
                    password=generate_password_hash(default_admin_password),
                    name='Admin',
                    firstname='User',
                    roles=[admin_role],  # Assign the admin role
                    role='Administrator'  # Set the role field explicitly
                )
            db.session.commit()

        from .controllers.auth_controller import auth_bp
        from .controllers.query_controller import query_bp
        from .routes.routes import api as routes_bp

        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(query_bp, url_prefix='/api/query')
        app.register_blueprint(routes_bp, url_prefix='/api')

        # Register error handlers
        from .error_handlers import register_error_handlers
        register_error_handlers(app)

        # Custom error logging
        @app.errorhandler(500)
        def internal_error(error):
            app.logger.error('Server Error: %s', (error))
            return jsonify({"error": "Internal server error"}), 500

        @app.errorhandler(Exception)
        def unhandled_exception(e):
            app.logger.error('Unhandled Exception: %s', (e))
            return jsonify({"error": "Internal server error"}), 500

    return app
