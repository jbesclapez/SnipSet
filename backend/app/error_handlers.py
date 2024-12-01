from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from . import db

def register_error_handlers(app):
    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(e):
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({"error": e.description}), e.code
        return jsonify({"error": "Internal server error"}), 500
