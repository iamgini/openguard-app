# syntax=docker/dockerfile:1
FROM python:3

## PYTHONDONTWRITEBYTECODE: Prevents Python from 
##   writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=1

## PYTHONUNBUFFERED: Prevents Python from 
##   buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --upgrade pip
WORKDIR /code/
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . .