FROM python:3.11-slim-buster

RUN apt-get update && apt-get install -y netcat && apt-get clean

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /star-burger/backend

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .
