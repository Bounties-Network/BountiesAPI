FROM ubuntu:16.04

RUN apt-get update \
	&&  apt-get -y install postgresql

WORKDIR /usr/src/app
COPY . .
