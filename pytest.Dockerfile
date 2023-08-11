FROM python:3.10-slim

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry

# Installing project dependecies
COPY pyproject.toml .
RUN poetry install

COPY . /app

ENTRYPOINT [ "poetry", "run", "pytest", "-vv" ]
#ENTRYPOINT [ "python", "-m", "http.server" ]
