# coding=utf-8
import os
from pyvirt import create_app
from flask import g
from flask_socketio import SocketIO
from pyvirt.resources.events import event_cb
from pyvirt.utils.libvirt import LibvirtEventConnector

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

config_name = os.getenv('FLASK_CONFIGURATION', 'development')
app = create_app(config_name)

socketio = SocketIO(
        app=app,
        async_mode=async_mode)


@app.teardown_appcontext
def teardown_conn(exception):
    conn = getattr(g, 'libvirt_conn', None)
    if conn is not None:
        conn.close()


@socketio.on('connect', namespace='/libvirt')
def on_io_connect():
    app.logger.info('SocketIO client connected')


@socketio.on('disconnect', namespace='/libvirt')
def on_io_disconnect():
    app.logger.info('SocketIO client disconnected')


def main():
    app.logger.info(config_name)

    conn = LibvirtEventConnector()
    conn.start_event_loop()
    conn.connect(app.config['XEN_URI'])
    conn.register_event_cb(
        cb=lambda *args: event_cb(socketio, *args)
    )

    socketio.run(app, port=app.config['PORT'] or 80, use_reloader=False, debug=True)


if __name__ == '__main__':
    main()
