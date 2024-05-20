FROM python:3.9.18-slim


ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install gdal-bin -y

COPY freeze-celery.txt /freeze-celery.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r /freeze-celery.txt

COPY ./LAMA_ucup ./app

WORKDIR /app