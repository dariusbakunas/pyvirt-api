FROM python:3
LABEL maintainer "bakunas@gmail.com"

RUN apt-get update -yqq && apt-get install -yqq \
	libvirt-dev python-pip

RUN UWSGI_PROFILE="asyncio" pip3 install uwsgi

RUN pip install pipenv --upgrade

WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system --deploy

EXPOSE 3031 3032
COPY . /app

CMD [ "uwsgi", "uwsgi.ini"]