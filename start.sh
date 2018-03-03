#!/bin/bash

export FLASK_APP=./app.py
export FLASK_DEBUG=1
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0