FROM python:3.7-alpine

RUN pip install flask-restplus

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]