FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN python -m venv ./venv
RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install pytest httpx pydicom

ENTRYPOINT [ "venv/bin/pytest", "-vv" ]

