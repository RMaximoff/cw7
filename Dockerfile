FROM python:3.11

WORKDIR /app

COPY ./requirements.txt .

RUN pip install requirements.txt

COPY . .