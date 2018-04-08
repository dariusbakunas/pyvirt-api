# coding=utf-8
import os
from pyvirt import create_app
from bg_tasks.tasks import start_libvirt_loop_task

config_name = os.getenv('FLASK_CONFIGURATION', 'development')
app, socketio = create_app(config_name)

bg_task = None

@socketio.on('connect', namespace='/libvirt')
def on_io_connect():
    global bg_task
    app.logger.info('SocketIO client connected')
    bg_task = start_libvirt_loop_task.delay(app.config['REDIS_URL'], app.config['XEN_URI'])


@socketio.on('disconnect', namespace='/libvirt')
def on_io_disconnect():
    # if bg_task:
    #     bg_task.revoke(terminate=True)
    app.logger.info('SocketIO client disconnected')


def main():
    socketio.run(app, port=app.config['PORT'] or 80, use_reloader=False, debug=True)


if __name__ == '__main__':
    main()
