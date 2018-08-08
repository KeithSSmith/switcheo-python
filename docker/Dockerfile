# Switcheo Python Development Environment - Dockerfile
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

# Disable DOTNET usage information collection
# https://docs.microsoft.com/en-us/dotnet/core/tools/telemetry#behavior
ENV DOTNET_CLI_TELEMETRY_OPTOUT 1

# Install system dependencies. always should be done in one line
# https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#run
RUN apt-get update && apt-get install -y \
    unzip \
    git-core \
    wget \
    curl \
    python3.6 \
    python3.6-dev \
    python3.6-venv \
    python3-pip \
    libleveldb-dev \
    libssl-dev \
    g++ && \
    cd /usr/local/bin && \
    ln -s /usr/bin/python3 python && \
    python -m pip install --upgrade pip && \
    pip install --upgrade pip

# APT cleanup to reduce image size
RUN rm -rf /var/lib/apt/lists/*

# Update Python environment based on required packages
COPY requirements.txt /
RUN python -m pip install -r /requirements.txt
