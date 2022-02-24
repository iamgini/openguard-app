# Oopen Guard - Security Automation

OpenGuard application source code

- [Oopen Guard - Security Automation](#oopen-guard---security-automation)
  - [Preparing the Containerization](#preparing-the-containerization)
    - [Create the `Dockerfile`](#create-the-dockerfile)
    - [Create the `requirements.txt`](#create-the-requirementstxt)
    - [Create `docker-compose.yml`](#create-docker-composeyml)
  - [Build the image](#build-the-image)
  - [Preparing the Django project](#preparing-the-django-project)
  - [Connect the database](#connect-the-database)
  - [Appendix](#appendix)


## Preparing the Containerization

### Create the `Dockerfile`

```python
# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
```

### Create the `requirements.txt`

```python
Django>=4.0
psycopg2>=2.8  # PostgreSQL database adapter for Python
```

### Create `docker-compose.yml`

```yaml
version: "3.9"
   
services:
  db:
    image: postgres
    volumes:
      - ./data/db:/var/lib/postgresql/data
    environment:
      - POSTGRES_NAME=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_NAME=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    depends_on:
    #  - db
```

## Build the image

```shell
$ podman build  .
```


## Preparing the Django project

```shell
## switch to project directory
$ cd 
openguard-app $ podman-compose run web django-admin startproject composeexample .
```

## Connect the database

```python
# settings.py
   
import os
   
[...]
   
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}
```

## Appendix