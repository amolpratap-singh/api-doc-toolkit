From python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/
COPY frontend/ frontend/
COPY config/ config/
COPY openapi_specs/ openapi_specs/

EXPOSE 5000

WORKDIR /app/backend

CMD ["python", "app.py"]
