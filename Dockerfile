FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /star-burger

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .
