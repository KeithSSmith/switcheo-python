FROM jfloff/alpine-python:3.6-slim AS build
ADD requirements*.txt /app/
WORKDIR /app
RUN apk add --no-cache --update python3-dev gcc musl-dev libffi-dev openssl-dev && \
    python -m pip install --upgrade pip setuptools wheel cryptography && \
    python -m pip install -r requirements.txt && \
    python -m pip install -r requirements_dev.txt && \
    python -m pip install -r requirements_pytest.txt && \
    rm -rf /var/cache/apk/*
ADD . /app
WORKDIR /app
