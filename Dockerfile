FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY dev_init_db.py .

ENV PYTHONAPP=/app
ENV ENVIRONMENT=production

EXPOSE 8000