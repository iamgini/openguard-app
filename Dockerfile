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
#USER openguard
RUN mkdir -pv /var/{log,run}/gunicorn/ 
#    && chown -cR openguard /var/{log,run}/gunicorn/

COPY . .

EXPOSE 8000

#CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "openguard.wsgi.applicationapplication"]
#CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "openguard.wsgi"]
CMD ["gunicorn", "-c", "config/gunicorn/dev.py"]
#CMD ["python", "-u", "manage.py", "runserver"]
#CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:8000"]