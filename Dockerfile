FROM python:3.13-slim
WORKDIR /app
COPY backend/pyproject.toml /app/
COPY backend/app /app/app
COPY backend/migrations /app/migrations
COPY backend/alembic.ini /app/
RUN pip install --no-cache-dir . && addgroup --system jahhezly && adduser --system --ingroup jahhezly jahhezly
RUN chown -R jahhezly:jahhezly /app
USER jahhezly
EXPOSE 8000
CMD ["/bin/sh","-c","alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips *"]
