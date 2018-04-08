FROM python:3
LABEL maintainer "bakunas@gmail.com"

RUN apt-get update -yqq && apt-get install -yqq \
	libvirt-dev python-pip

RUN pip install pipenv --upgrade

WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system --deploy

EXPOSE 8000
COPY . /app

CMD [ "gunicorn", "-c", "gunicorn.py", "app:app"]