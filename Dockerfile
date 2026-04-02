FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md wsgi.py ./
COPY src/ src/
COPY templates/ templates/
COPY static/ static/

RUN pip install --no-cache-dir ".[web]" gunicorn

EXPOSE 8000

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "30"]
