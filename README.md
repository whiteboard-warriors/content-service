Content microservice for the Whiteboard Warriors website

## Tech Stack
- Python
- Flask - lightweight micro web framework written in Python
- Flask-Restplus - Flask extension for building REST APIs with swagger documentation
- PostgreSQL - open source object-relational database system
- SQLAlchemy - open-source SQL toolkit and object-relational mapper for the Python


## Installation
```
# Clone repository
$ git clone https://github.com/whiteboard-warriors/content-service
$ cd content-service

# Create virtual environment
$ python -m venv env

# Activate the environment
$ source env/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Create database 'whiteboardwarriors-contentdb'
$ createdb whiteboardwarriors-contentdb


# Create .env file for your environment variables
# Sample content of .env file:

POSTGRES_HOST=localhost
POSTGRES_DB=whiteboardwarriors-contentdb
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_PORT=5432

# Initialize database
$ python -i init_db.py

# Run server
$ python server.py
```

## Building content service container

```
$ docker build -f docker/app/Dockerfile --tag contents-service .

Successfully built a89a6039f692
Successfully tagged contents-service:latest
```

```
$ docker images | head

REPOSITORY        TAG        IMAGE ID           CREATED              SIZE
contents-service  latest     a89a6039f692       About a minute ago   149MB
<none>            <none>     eae74fb29362       2 minutes ago        413MB
alpine            3.9        82f67be598eb       5 weeks ago          5.53MB
```


## Run the container
#### To access the internal port 8000, route it with the -p option.
```
$ docker run -it -p 127.0.0.1:8000:8000/tcp content-service
```

## Stop the container
```
# Show currently running container
$ docker ps

CONTAINER ID        IMAGE               COMMAND
0f822478f63e        contents-service    "/bin/sh /opt/uwsgi/…"

$ docker stop 0f822478f63e
```