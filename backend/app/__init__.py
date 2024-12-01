from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_babel import Babel
from .config.db_config import Config  # Updated import to use db_config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register models to ensure they are part of SQLAlchemy
    from .models.models import (
        User, Role, Category, Subcategory, Snippet, Tag,
        SnippetTag, Comment, AuditLog, OAuthToken, FailedLogin,
        Backup, AITrainingExport
    )
    
    CORS(app)
    Babel(app)

    # Register blueprints
    from .routes.routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app
