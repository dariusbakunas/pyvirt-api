# coding=utf-8
from flask import Flask
from celery import Celery
from pyvirt.config import app_config
from flask_restful import Api
from flask_socketio import SocketIO
from pyvirt.resources.domain import DomainList
from pyvirt.resources.events import event_cb
from pyvirt.utils.libvirt import LibvirtEventConnector

import eventlet
eventlet.monkey_patch()

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = 'eventlet'
socketio = SocketIO()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py', silent=True)

    app.logger.info(config_name)

    # conn = LibvirtEventConnector(logger=app.logger)
    # # conn.start_aio_loop()
    # conn.start_native_loop()
    # # conn.start_pure_loop()
    # conn.connect(app.config['XEN_URI'])
    # conn.register_event_cb(
    #     cb=lambda *args: event_cb(socketio, app.logger, *args)
    # )

    api = Api(app)
    api.add_resource(DomainList, '/api/domain')
    celery = Celery(app.name, broker=app.config['BROKER_URL'])
    celery.conf.update(app.config)
    socketio.init_app(app, async_mode=async_mode, message_queue=app.config['REDIS_URL'])

    return app, socketio, celery
