FROM python:3.10-bullseye AS builder

ARG REQUIREMENTS=dev.txt
ENV REQUIREMENTS=$REQUIREMENTS

COPY ./requirements/$REQUIREMENTS /requirements/$REQUIREMENTS

RUN apt-get update \
    && apt-get --yes upgrade \
    && apt-get --yes install --no-install-recommends libpq-dev \
    && python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python -m pip wheel --requirement /requirements/$REQUIREMENTS --wheel-dir /wheels


FROM python:3.10-slim-bullseye AS final

WORKDIR /app

ARG ENVIRONMENT=dev
ENV ENVIRONMENT=$ENVIRONMENT

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder ./wheels/ /wheels/

RUN apt-get update \
    && apt-get --yes upgrade \
    && apt-get --yes install --no-install-recommends libpq5 wait-for-it \
    && python -m pip install --no-cache-dir --upgrade pip setuptools wheel debugpy \
    && python -m pip install --no-cache-dir /wheels/* \
    && apt-get --yes autoremove \
    && apt-get --yes autoclean \
    && apt-get --yes clean \
    && rm -rf ./wheels \
    && rm -rf /var/lib/apt/lists/*
