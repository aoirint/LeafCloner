FROM python:3

WORKDIR /work

RUN apt update && apt install -y\
  wait-for-it

ADD requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

ADD code/ /code
