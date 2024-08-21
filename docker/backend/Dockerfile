FROM python:latest

WORKDIR /app

RUN apt-get update -yy && apt-get install -y tini

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["tini", "--"]
CMD ["gunicorn", "python.io_atomgroup.soccer"]
