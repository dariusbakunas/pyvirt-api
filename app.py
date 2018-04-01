# coding=utf-8
import os
from pyvirt import create_app


config_name = os.getenv('FLASK_CONFIGURATION', 'development')
app, socketio = create_app(config_name)


@socketio.on('connect', namespace='/libvirt')
def on_io_connect():
    app.logger.info('SocketIO client connected')


@socketio.on('disconnect', namespace='/libvirt')
def on_io_disconnect():
    app.logger.info('SocketIO client disconnected')


def main():
    socketio.run(app, port=app.config['PORT'] or 80, use_reloader=False, debug=True)


if __name__ == '__main__':
    main()
