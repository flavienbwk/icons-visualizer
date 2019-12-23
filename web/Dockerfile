FROM node:13.0.1

WORKDIR '/app'

COPY ./app/package.json /app/package.json
RUN npm install

CMD [ "npm", "run", "start" ]