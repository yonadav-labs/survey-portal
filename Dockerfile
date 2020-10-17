FROM python:3.8.6

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt
