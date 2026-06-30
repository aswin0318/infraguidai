FROM python:3.12-slim

WORKDIR /app

# Install the shared library first (better layer caching)
COPY shared /shared
RUN pip install --no-cache-dir /shared

COPY services/ingestion-service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/ingestion-service/app ./app

EXPOSE 8003
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
