FROM python:latest

WORKDIR /app

RUN apt-get update -yy && apt-get install -y tini less iputils-ping net-tools netcat-traditional

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

COPY deps/django-celery-beat-fork deps/django-celery-beat-fork
COPY requirements.txt .
RUN pip3 install -r requirements.txt
# RUN ipython3 profile create

ENTRYPOINT ["tini", "--"]
CMD ["bash", "docker/backend/serve.sh"]
