# API Documentation Generator Toolkit

## 🚀 Features

- **Generate Interactive HTML Documentation** 
 
  Automatically generate a rich, interactive HTML page for your API using provided OpenAPI schema files.

- 📂 **Support for Multiple File Types**  
  Accepts `.yaml`, `.yml`, and `.json` schema files—either as a single file or multiple files in a directory.

- 🔧 **Executable API Interface**  
  The generated HTML allows developers to try out API calls directly from the documentation (e.g., using Swagger UI or Redoc with Try-It-Out).

- 🎨 **Customizable Documentation**  
  Prefilled OpenAPI templates and example YAML files let you create custom, branded documentation easily.

- 🧪 **Add Static Samples**  
  Embed static example requests/responses for clarity and usage reference.

---

## ⚙️ Command Line Parameters

| Parameter         | Description                           |
|------------------|---------------------------------------|
| `--input`         | Path to OpenAPI schema file or folder |
| `--output`        | Output path for the generated HTML    |
| `--env`           | Path to environment config (`.env`, `.json`, or `.yaml`) |
| `--merge`         | Optional flag to merge multiple files |
| `--static-samples`| Folder path containing static examples |

---

## 🌍 Environment Variables

The toolkit supports environment variable injection into the OpenAPI schema using placeholders such as `{{BASE_URL}}`, `{{AUTH_TOKEN}}`, etc.

You can define environment variables via:

- A `.env` file  
- A `config/env.json` or `config/env.yaml` file  
- Directly in your shell before running the tool

---

## 🛠 Configuration File

Example `env.json`:

```json
{
  "BASE_URL": "https://api.example.com",
  "AUTH_TOKEN": "Bearer your-token"
}
