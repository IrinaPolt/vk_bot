FROM postgres:latest

COPY init.sql /docker-entrypoint-initdb.d/
COPY data_files/. /docker-entrypoint-initdb.d/

ENV POSTGRES_DB=${POSTGRES_DB}
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
