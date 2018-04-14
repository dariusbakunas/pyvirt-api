FROM python:3
LABEL maintainer "bakunas@gmail.com"

RUN apt-get update -yqq && apt-get install -yqq \
	libvirt-dev

RUN pip install pipenv --upgrade

WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system --deploy

COPY bg_tasks /app/bg_tasks
COPY worker.py /app

CMD [ "python", "./worker.py" ]