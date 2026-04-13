import os
import json
import yaml
from pathlib import Path

SPEC_DIR = Path(__file__).parent.parent.parent / "specs"
VALID_EXT = {".json", ".yaml", ".yml"}

def list_specs():
    """
    List all available spec files in the specs directory.
    """
    
    if not SPEC_DIR.exists():
        return []
    
    return [f.name for f in SPEC_DIR.iterdir() if f.suffix.lower() in VALID_EXT]

def parse_spec(file_name):
    """
    Parse an OpenAPI spec file and return its content in structured data format.
    """
    file_path = SPEC_DIR / file_name
    
    if not file_path.exists():
        raise FileNotFoundError(f"Spec file '{file_name}' not found.")
    
    raw = file_path.read_text(encoding='utf-8')
    if file_path.suffix.lower() == ".json":
        # with open(file_path, 'r') as f:
        #     return json.load(f)
        spec = json.loads(raw)
    elif file_path.suffix.lower() in {".yaml", ".yml"}:
        # with open(file_path, 'r') as f:
        #     return yaml.safe_load(f)
        spec = yaml.safe_load(raw)
    else:
        raise ValueError(f"Unsupported file extension '{file_path.suffix}'.")
    return normalize_spec(spec)

def normalize_spec(spec):
    """
    Normalize the spec data to ensure consistent structure for downstream processing.
    Normalize both Swagger 2.0 and OpenAPI 3.x 
    This can include:
    - Ensuring all paths are in a consistent format
    - Converting any relative references to absolute ones
    - Validating required fields and adding defaults if necessary
    """
    info = spec.get("info", {})
    result = {
        "title": info.get("title", "Untitled API"),
        "version": info.get("version", ""),
        "description": info.get("description", ""),
        "base_uri": _extract_base_uri(spec),
        "endpoints": [],
        "components": spec.get("components", {}),  # For OpenAPI 3.x
        "definitions": spec.get("definitions", {}) or _extract_schemas(spec),   # For Swagger 2.0    
    }
    
    for path, methods in spec.get("paths", {}).items():
        for method, details in methods.items():
            if method.startswith("x-") or method == "parameters":  # Skip vendor extensions and global parameters
                continue
            endpoint = {
                "path": path,
                "method": method.upper(),
                "summary": details.get("summary", ""),
                "description": details.get("description", ""),
                "parameters": details.get("parameters", []),
                "requestBody": _extract_request_body(details),
                "responses": details.get("responses", {}),
                "tags": details.get("tags", []),
            }
            result["endpoints"].append(endpoint)
    return result

def _extract_base_uri(spec):
    """
    Extract the base URI from the spec, handling both Swagger 2.0 and OpenAPI 3.x formats.
    """
    if "servers" in spec:  # OpenAPI 3.x
        return spec["servers"][0].get("url", "")
    elif "host" in spec and "schemes" in spec:  # Swagger 2.0
        scheme = spec["schemes"][0] if isinstance(spec["schemes"], list) else spec["schemes"]
        return f"{scheme}://{spec['host']}{spec.get('basePath', '')}"
    return ""

def _extract_request_body(details):
    """
    Extract the request body from the endpoint details, handling both Swagger 2.0 and OpenAPI 3.x formats.
    """
    # OpenAPI 3.x requestbody
    rb = details.get("requestBody")
    if rb:
        content = rb.get("content", {})
        json_body = content.get("application/json", {})
        return json_body.get("schema", {})
    # Swagger 2.0 body parameter
    for p in details.get("parameters", []):
        if p.get("in") == "body":
            return p.get("schema", {})
    return None

def _extract_schemas(spec):
    """
    Extract schemas from OpenAPI 3.x spec, which are defined under 'components/schemas'.
    """
    return spec.get("components", {}).get("schemas", {})