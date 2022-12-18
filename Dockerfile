# FROM ubuntu:latest
# RUN apt-get update -y
# RUN apt-get install -y python3 python3-pip
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# CMD ["flask", "run"]

FROM python:3

WORKDIR /app
COPY app.py /app
COPY auth_decorator.py /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD python app.py