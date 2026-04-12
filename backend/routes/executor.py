import requests as http_requests
from flask import Blueprint, request, jsonify

from services.env_loader import load_env
from models.database import save_sample

executor_bp = Blueprint("executor", __name__)

@executor_bp.route("/", methods=["POST"])
def execute_api():
    """
    Endpoint to execute an API request based on the provided OpenAPI spec details.
    Proxy an API Call.
    Expects a JSON body with the following structure:
    {
        "method": "GET|POST|PUT|DELETE",
        "url": "https://api.example.com/data",
        "headers": {"Authorization": "Bearer token"},
        "body": {"key": "value"},
        "spec_file": "optional_spec_file.yaml",
        "path": "..."
    }
    """
    data = request.get_json()
    method = data.get("method", "GET").upper()
    url = data.get("url")
    headers = data.get("headers", {})
    body = data.get("body", {})
    spec_file = data.get("spec_file", "")
    api_path = data.get("path", "")

    if not method or not url:
        return jsonify({"error": "Method and URL are required"}), 400

    # Load environment variables for authentication
    env_vars = load_env()
    for key, value in env_vars.items():
        uri = uri.replace(f"{{{key}}}", value)
        headers = {k: v.replace(f"{{{key}}}", value) for k, v in headers.items()}
    # headers.update(env_vars)

    try:
        resp = http_requests.request(method, url, headers=headers, json=body if body else None, timeout=30)
        try:
            resp_body = resp.json()
        except ValueError:
            resp_body = resp.text

        # Auto-save successful responses as samples
        if resp.ok and spec_file:
            # Save the sample request and response to the database
            save_sample(
                spec_file=spec_file,
                path=api_path,
                method=method,
                request_body=body,
                response_status=resp.status_code,
                response_body=resp_body
            )
        return jsonify({
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
            "body": resp_body
        })
    except http_requests.exceptions.ConnectionError:
        return jsonify({"error": "Connection failed. Check the URL."}), 502
    except http_requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500