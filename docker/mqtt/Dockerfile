FROM eclipse-mosquitto

RUN apk add tini
USER root
ENTRYPOINT ["tini", "--"]
CMD ["sh", "/app/docker/mqtt/serve.sh"]
