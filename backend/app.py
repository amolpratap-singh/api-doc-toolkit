import os
import logging
from flask import Flask
from flask_cors import CORS

from models.database import init_db

from routes.schema import schema_bp
from routes.executor import executor_bp
from routes.samples import samples_bp

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = Flask(__name__, static_folder="../frontend", static_url_path="/" )
CORS(app)

init_db()

app.register_blueprint(schema_bp, url_prefix="/api/schema")
app.register_blueprint(executor_bp, url_prefix="/api/execute")
app.register_blueprint(samples_bp, url_prefix="/api/samples")

if __name__ == "__main__":
    app.run(debug=True, port=5000)