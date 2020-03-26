# Dockerfile for localdev purposes only, so it
# won't be optimized for size
FROM alpine:3.9

# Add the proper env variables for initializing the db
ARG POSTGRES_DB
ENV POSTGRES_DB $POSTGRES_DB
ARG POSTGRES_USER
ENV POSTGRES_USER $POSTGRES_USER
ARG POSTGRES_PASSWORD
ENV POSTGRES_PASSWORD $POSTGRES_PASSWORD
ARG POSTGRES_PORT
ENV LANG en_US.utf8
EXPOSE $POSTGRES_PORT

# For usage in startup
ENV POSTGRES_HOST localhost
ENV DATABASE_ENGINE POSTGRESQL
# Store the data inside the container, as we don't care for persistence
RUN mkdir -p /opt/data
RUN chown -R postgres /opt/data
ENV PGDATA /opt/data


# Install postgresql pkg and all its dependencies
RUN apk update
RUN apk add bash curl su-exec python3
RUN apk add postgresql postgresql-contrib postgresql-dev
RUN apk add python3-dev build-base linux-headers gcc libffi-dev


# Adding our code
WORKDIR /opt/src

RUN mkdir -p /opt/src/db
# Add postgres setup
ADD ./docker/db/postgres-setup.sh /opt/src/db/
RUN chmod +x /opt/src/db/postgres-setup.sh
RUN /opt/src/db/postgres-setup.sh

# Install our code to prepare the DB
ADD ./ContentService/requirements.txt /opt/src

RUN pip3 install -r requirements.txt

# Need to import all the code, due dependencies to initialise the DB
ADD ./ContentService/ /opt/src/
# Add all DB commands
ADD ./docker/db/* /opt/src/db/

# get the db ready
RUN chmod +x /opt/src/db/prepare_db.sh
RUN chmod +x /opt/src/db/start_postgres.sh
RUN chmod +x /opt/src/db/stop_postgres.sh
RUN /opt/src/db/prepare_db.sh

# Start the database in normal operation
USER postgres
CMD ["postgres"]

