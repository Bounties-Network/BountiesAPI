FROM ubuntu:16.04

# Install cron

RUN apt-get update \
	&&  apt-get -y install postgresql

WORKDIR /usr/src/app
COPY . .
