FROM python:alpine
MAINTAINER Benoît Pourre <benoit.pourre@gmail.com>

RUN pip install --upgrade pip pyownet influxdb PyYAML

ADD get_temp.py /
ADD conf.yml_template /conf.yml

WORKDIR /
CMD python -u /get_temp.py
