from flask import Blueprint, jsonify, request
from models.database import get_sampels, delete_samples, save_sample

samples_bp = Blueprint("samples", __name__)

@samples_bp.route("/", methods=["GET"])
def list_samples():
    """
    Endpoint to list all saved API request/response samples.
    Optional query parameter: ?spec_file=filename.yaml to filter by spec file.
    """
    spec_file = request.args.get("spec_file")
    return jsonify(get_sampels(spec_file))

@samples_bp.route("/", methods=["POST"])
def create_sample():
    """
    Endpoint to create a new API request/response sample.
    Manually create a sample by providing the necessary details in the request body.
    Expects a JSON body with the following structure:
    {
        "spec_file": "filename.yaml",
        "path": "/api/data",
        "method": "GET|POST|PUT|DELETE",
        "request_body": {"key": "value"},
        "response_status": 200,
        "response_body": {"result": "success"}
    }
    """
    data = request.get_json()
    required = ["spec_file", "path", "method"]
    if not all(data.get(f) for f in required):
        return jsonify({"error": f"Missing required fields: {', '.join(required)}"}), 400

    save_sample(
        spec_file=data["spec_file"],
        path=data["path"],
        method=data["method"],
        request_body=data.get("request_body"),
        response_status=data.get("status_code"),
        response_body=data.get("response_body")
    )

    return jsonify({"message": "Sample saved successfully"}), 201

@samples_bp.route("/<int:sample_id>", methods=["DELETE"])
def delete_sample(sample_id):
    """
    Endpoint to delete a specific sample by its ID.
    """
    delete_samples(sample_id)
    return jsonify({"message": "Sample deleted successfully"}), 200