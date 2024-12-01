# app/controllers/query_controller.py

from flask import request, jsonify, Blueprint
from app import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

query_bp = Blueprint('query_bp', __name__)

@query_bp.route('/', methods=['POST'])
def execute_query():
    data = request.get_json()
    table_name = data.get('table_name')
    sql_query = data.get('sql_query')

    if not table_name or not sql_query:
        return jsonify({"error": "Table name and SQL query are required"}), 400

    try:
        # Safely format the query
        sql_query = text(sql_query.format(table_name=table_name))

        result = db.session.execute(sql_query)
        records = [dict(row) for row in result.mappings()]  # Correctly convert rows to dictionaries

        return jsonify(records), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
