FROM node:13.0.1-alpine

ARG NODE_ENV
ARG REACT_APP_API_ENDPOINT

COPY ./app /app

WORKDIR '/app'
RUN npm install
RUN npm run build --production

RUN npm install -g serve

EXPOSE 80
ENTRYPOINT ["serve", "-l", "tcp://0.0.0.0:80", "-s", "/app/build"]
