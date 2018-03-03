FROM tiangolo/uwsgi-nginx-flask:python3.6
RUN pip install pipenv --upgrade

RUN apt-get update -yqq && apt-get install -yqq \
	libvirt-dev

WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system --deploy

COPY . /app