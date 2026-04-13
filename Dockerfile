FROM python:3.12-slim

# 1. OS(Linux) 側の設備を整える
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    tree \
    git \
    python3-tk \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/study_box

# ライブラリを一括インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
