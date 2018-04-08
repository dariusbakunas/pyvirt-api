FROM python:3
LABEL maintainer "bakunas@gmail.com"

RUN apt-get update -yqq && apt-get install -yqq \
	libvirt-dev python-pip

RUN pip install pipenv --upgrade

WORKDIR /worker

ENV CELERY_BROKER_URL=redis://redis:6379/0

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system --deploy

COPY bg_tasks/ /worker

ENTRYPOINT celery -A tasks worker --loglevel=info
