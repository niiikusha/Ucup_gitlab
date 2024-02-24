FROM python:3.9.18-slim

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install gdal-bin gettext libgettextpo-dev libpq-dev cmake -y

COPY freeze.txt /freeze.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r /freeze.txt

COPY ./LAMA_ucup ./app

COPY ./docker/app/start.sh /start
RUN chmod +x /start
RUN sed -i 's/\r//' /start
RUN chmod 755 /start

WORKDIR /app
