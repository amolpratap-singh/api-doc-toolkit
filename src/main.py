import os
import logging
from pathlib import Path

from utils.file_utils import APISpecFileUtility

# Logging Configuration
log_level = os.getenv("LOG_LEVEL", "INFO")
logger = logging.getLogger("ApiDocToolkit")
format = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(format)
logger.addHandler(handler)
logger.setLevel(log_level)
logger.propagate = False

DEFAULT_CONFIG = {
    "api_spec_dir": Path(__file__).parent.parent.joinpath("openapi"),
    "config_dir": Path(__file__).parent.parent.joinpath("config"),
    "output_dir": Path(__file__).parent.parent.joinpath("output"),
    "log_level": log_level,
}

class APIDocumentationGenerator:

    def __init__(self):
        self.config_dir = os.getenv("CONFIG_DIR", DEFAULT_CONFIG.get("config_dir"))
        logger.debug(f"Configuration directory set to: {self.config_dir}")
        self.api_spec_dir = os.getenv("API_SPEC_DIR", DEFAULT_CONFIG.get("api_spec_dir"))
        logger.debug(f"API specification directory set to: {self.api_spec_dir}")

    def generate_api_docs(self)-> None:
        """
        Generate API documentation based on the specifications provided.
        This method will read the API specifications from the specified directory
        and generate documentation in the desired format (e.g., Markdown, HTML).
        It can be extended to support various formats and styles as needed.

        The generated documentation can be used for both internal and external purposes,
        such as developer guides, API references, and user manuals.
        The implementation can utilize libraries like OpenAPI Generator, Swagger UI,
        or custom scripts to parse the API specifications and create the documentation.

        The generated documentation will be stored in a specified output directory,
        which can be configured through environment variables or passed as parameters.
        This method is designed to be flexible and extensible, allowing for future enhancements
        and support for additional features such as versioning, localization, and theming.

        :return: None
        :rtype: None
        """
        logger.info("Generating API documentation...")
        try:
            api_spec_util = APISpecFileUtility(self.api_spec_dir)
            file_list = api_spec_util.get_spec_files()
        except Exception as e:
            logger.error(f"Error retrieving API specification files: {e}")
            return
        logger.info(f"Found {len(file_list)} API specification files.")

        #logger.info("API documentation generated successfully.")


if __name__ == "__main__":
    logger.info("Starting API Documentation Toolkit...")
    APIDocumentationGenerator().generate_api_docs()
