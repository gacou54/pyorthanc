ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry

# Installing project dependecies
COPY ../../pyproject.toml .
RUN poetry install --extras "all" --no-root

COPY ../.. /app

ENTRYPOINT [ "poetry", "run", "pytest", "-vv"]
