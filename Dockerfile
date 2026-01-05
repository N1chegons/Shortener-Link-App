FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==1.8.3"

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY src ./src

COPY migrations ./migrations

COPY alembic.ini .

CMD ["sh", "-c", "\
  echo '🚀 Starting FastAPI application' && \
  echo '⏳ Waiting for database...' && \
  sleep 5 && \
  echo '📦 Running migrations...' && \
  alembic revision --autogenerate && \
  alembic upgrade head && \
  echo '✅ Starting server...' && \
  echo '📄 Docs: http://localhost:5050/docs' && \
  uvicorn src.main:app --host 0.0.0.0 --port 8000"]

