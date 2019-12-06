FROM golang

#インストール
RUN apt-get update
RUN apt-get install -y sudo
RUN sudo apt-get install -y vim

RUN cd /go/src && mkdir go_weather
ADD setup.sh /go/

WORKDIR /go/src/go_weather
RUN go get gopkg.in/ini.v1

# CMD ["/sbin/init"]
# CMD ["./go_weather"]
# CMD ["sh setup.sh"]
