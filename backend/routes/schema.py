from flask import Blueprint, jsonify, request
from services.spec_parser import parse_spec, list_specs

schema_bp = Blueprint("schema", __name__)

@schema_bp.route("/files", methods=["GET"])
def get_spec_files():
    """
    Endpoint to list all available OpenAPI spec files.
    """
    return jsonify(list_specs())

@schema_bp.route("/parse", methods=["GET"])
def get_parsed_spec():
    """
    Parse and return a specific OpenAPI spec file.
    Query parameter:    ?file=filename
    """
    file_name = request.args.get("file")
    if not file_name:
        return jsonify({"error": "File name parameter is required"}), 400

    try:
        return jsonify(parse_spec(file_name))
    except FileNotFoundError:
        return jsonify({"error": "Specified file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500