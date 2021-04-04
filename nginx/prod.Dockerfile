FROM nginx:1.18

RUN rm /etc/nginx/conf.d/default.conf
COPY ./icons-visualizer.conf /etc/nginx/conf.d/icons-visualizer.conf

CMD ["nginx", "-g", "daemon off;"]