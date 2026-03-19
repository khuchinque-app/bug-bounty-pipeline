FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    subfinder \
    httpx \
    nuclei \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/
COPY data/ ./data/
COPY main.py .

ENTRYPOINT ["python", "main.py"]
