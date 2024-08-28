FROM ubuntu:latest

RUN apt-get update -yy && apt-get install -yy nginx libnginx-mod-rtmp tini

RUN ln -T -sf /app/docker/nginx/nginx.conf /etc/nginx/nginx.conf


RUN useradd nginx

ENTRYPOINT ["tini", "--"]
CMD ["nginx", "-g", "daemon off;"]
