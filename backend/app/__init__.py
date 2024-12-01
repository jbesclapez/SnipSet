from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_babel import Babel
from .config.db_config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models to ensure they are registered with SQLAlchemy
    from .models.models import User, Role, Category, Subcategory, Snippet, Tag, SnippetTag, Comment, AuditLog, OAuthToken, FailedLogin, Backup, AITrainingExport
    
    CORS(app)
    Babel(app)

    # Import and register the API blueprint
    from .routes.routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app
