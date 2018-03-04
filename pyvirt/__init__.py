# coding=utf-8
from flask import Flask
from flask_restful import Api
from pyvirt.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py', silent=True)

    api = Api(app)

    with app.app_context():
        from pyvirt.resources.domain import DomainList, Domain
        api.add_resource(DomainList, '/api/domain')
        api.add_resource(Domain, '/api/domain/<string:uuid>')

    return app
