FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml /app/
COPY app /app/app
COPY migrations /app/migrations
COPY alembic.ini /app/
RUN pip install --no-cache-dir .
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
