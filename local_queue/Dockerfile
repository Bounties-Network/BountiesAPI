FROM openjdk:8-alpine

ENV ELASTIC_MQ_VERSION 0.13.8

ADD https://s3.amazonaws.com/consensys_bounties/custom-fifo-mqserver-0.13.8.jar /custom-fifo-mqserver-0.13.8.jar
COPY elasticmq.conf /elasticmq.conf

ENTRYPOINT ["/usr/bin/java", "-Dconfig.file=elasticmq.conf", "-jar", "/custom-fifo-mqserver-0.13.8.jar"]

EXPOSE 9324
