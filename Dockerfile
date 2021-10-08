FROM python:3.9.4-slim-buster

RUN apt update -y && apt install git -y

WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
RUN pip install -r requirements.txt
