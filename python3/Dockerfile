FROM python:3.7
#FROM ubuntu:18.04

#インストール
#RUN apt-get update
#RUN apt-get install -y git
#RUN apt-get install -y iproute2
#RUN apt-get install -y iputils-ping
#RUN apt-get install -y sudo
#RUN sudo apt install python3.7

#geckodriverが必要か。

ADD requirements.txt /var/www/html/
WORKDIR /var/www/html/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# RUN pip install pipenv
