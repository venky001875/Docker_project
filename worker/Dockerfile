FROM python:3.12-slim

# Force Python to stream print logs instantly to Docker terminal
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "worker.py"]