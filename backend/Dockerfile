FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Set environment variables (optional)
ENV PYTHON_UNBUFFERED=1
ENV PYTHON_FAST_SITE=1

COPY src/alembic /app/alembic
COPY src/database.py /app/src/database.py
COPY src/config.py /app/src/config.py
RUN pip install alembic psycopg2-binary
CMD ["/bin/sh","-c","alembic -c src/alembic.ini upgrade head && exec uvicorn src.app:app --host 0.0.0.0 --port 8000"]