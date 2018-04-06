FROM nginx:1.13.8

RUN rm /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir -p /usr/src/app/project/static

COPY nginx.conf /etc/nginx/
COPY bfex.conf /etc/nginx/conf.d/

COPY static/index.html /usr/src/app/project/static
COPY static/batch.html /usr/src/app/project/static
