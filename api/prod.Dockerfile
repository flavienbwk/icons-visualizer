FROM python:3.7-alpine

RUN apk update && apk add libmagic

ARG FLASK_ENV

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Install WSGI server
RUN pip install gunicorn==20.1.0

WORKDIR /app
COPY ./app /app

# Run WSGI server with 3 workers
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5000", "app:app" ]
