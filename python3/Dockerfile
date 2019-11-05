FROM python:3.7

#インストール
RUN apt-get update
RUN apt-get install -y sudo
RUN sudo apt-get install -y vim

#geckodriverが必要か。

ADD requirements.txt /var/www/html/
WORKDIR /var/www/html/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /var/www/html/application

# CMD ["/sbin/init"]
CMD ["gunicorn", "server:app", "-b", "0.0.0.0:5000"]
