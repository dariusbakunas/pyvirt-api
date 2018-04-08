FROM python:3
LABEL maintainer "bakunas@gmail.com"

RUN apt-get update -yqq && apt-get install -yqq \
	libvirt-dev python-pip

RUN pip install pipenv --upgrade

WORKDIR /worker

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system --deploy

COPY bg_tasks/ /worker

ENTRYPOINT celery -A tasks worker --loglevel=info