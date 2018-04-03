# coding=utf-8
from flask import Flask
from pyvirt.config import app_config
from flask_restful import Api
from flask_socketio import SocketIO
from pyvirt.resources.domain import DomainList
from pyvirt.resources.events import event_cb
from pyvirt.utils.libvirt import LibvirtEventConnector

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None
socketio = SocketIO()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py', silent=True)

    app.logger.info(config_name)

    conn = LibvirtEventConnector(logger=app.logger)
    conn.start_event_loop()
    conn.connect(app.config['XEN_URI'])
    conn.register_event_cb(
        cb=lambda *args: event_cb(socketio, app.logger, *args)
    )

    DomainList.set_libvirt_conn(conn.libvirt_conn)

    api = Api(app)
    api.add_resource(DomainList, '/api/domain')

    socketio.init_app(app, async_mode=async_mode)

    return app, socketio
