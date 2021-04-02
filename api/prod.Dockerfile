FROM python:3.7-alpine

RUN apk update && apk add libmagic

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app
ENTRYPOINT [ "python", "/app/app.py" ]
