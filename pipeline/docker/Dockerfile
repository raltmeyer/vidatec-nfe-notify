FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean;

WORKDIR /app

COPY MyEvents.jar /app/MyEvents.jar

ENV DATABASE_URL=${DATABASE_URL}
ENV DATABASE_USER=${DATABASE_USER}
ENV DATABASE_PASSWORD=${DATABASE_PASSWORD}

EXPOSE 80

ENTRYPOINT ["java", "-jar", "/app/MyEvents.jar"]