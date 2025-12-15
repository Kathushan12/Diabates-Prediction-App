FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy backend code
COPY backend/ /app/backend/

# Install dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Create runtime folder for SQLite fallback (optional)
RUN mkdir -p /app/backend/data

EXPOSE 8000

# IMPORTANT:
# - bind to 0.0.0.0 so cloud can reach it
# - use $PORT if the platform sets it
CMD ["sh", "-c", "cd /app/backend && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

