# coding=utf-8
import os
from pyvirt import create_app
from flask import g


config_name = os.getenv('FLASK_CONFIGURATION', 'development')
app, socketio = create_app(config_name)


@socketio.on('connect', namespace='/libvirt')
def on_io_connect():
    app.logger.info('SocketIO client connected')


@socketio.on('disconnect', namespace='/libvirt')
def on_io_disconnect():
    app.logger.info('SocketIO client disconnected')


@app.teardown_appcontext
def teardown_conn(exception):
    conn = getattr(g, 'libvirt_conn', None)
    if conn is not None:
        app.logger.info('Closing libvirt connection')
        conn.close()


def main():
    socketio.run(app, port=app.config['PORT'] or 80, use_reloader=False, debug=True)


if __name__ == '__main__':
    main()
