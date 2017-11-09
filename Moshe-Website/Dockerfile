FROM ubuntu:17.10

MAINTAINER Moshe Silverstein <moshe.silverstein@mssm.com>

RUN apt-get update && apt-get install -y python3
RUN apt-get update && apt-get install -y python3-pip
RUN apt-get update && apt-get install -y python3-dev

RUN pip3 install --upgrade pip
RUN pip3 install flask
RUN pip3 install flask-sqlalchemy
RUN pip3 install flask-bcrypt
RUN pip3 install flask-mail
RUN pip3 install flask-login
RUN pip3 install flask-wtf
RUN pip3 install Flask-MySQL
RUN pip3 install mysql-connector-python-rf

RUN mkdir bionetbay
COPY . /bionetbay
WORKDIR bionetbay

RUN rm config.py

ENTRYPOINT python3 run.py
