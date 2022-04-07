FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml poetry.lock /
RUN pip install poetry && \
    python -m venv /.venv && \
    poetry install --no-dev

WORKDIR /app
ENTRYPOINT ["./entrypoint.sh"]
