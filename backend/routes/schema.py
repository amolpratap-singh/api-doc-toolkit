import os

from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

from services.spec_parser import parse_spec, list_specs, SPEC_DIR, VALID_EXT

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

# TODO: As this upload mechanism is storing the schema file into the directory 
# and not in the database, we need to implement a mechanism 
# to remove the file when the user deletes the schema from the UI.
@schema_bp.route("/upload", methods=["POST"])
def upload_spec_file():
    """
    Endpoint to upload one or more OpenAPI spec files. (.yaml, .yml or .json)
    """
    if "files" not in request.files:
        return jsonify({"error": "No files provided"}), 400
    
    SPEC_DIR.mkdir(parents=True, exist_ok=True)
    saved = []

    for f in request.files.getlist("files"):
        name = secure_filename(f.filename)
        ext = os.path.splitext(name)[1].lower()
        if ext not in VALID_EXT:
            continue
        
        dest = SPEC_DIR / name
        f.save(str(dest))
        saved.append(name)

    if not saved:
        return jsonify({"error": "No valid spec files uploaded"}), 400
    return jsonify({"message": f"Uploaded files: {', '.join(saved)} and saved {len(saved)} files"}), 201
