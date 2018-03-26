# coding=utf-8
import os
from pyvirt import create_app
from flask import render_template, g
from flask_socketio import SocketIO
from flask_restful import Api
from pyvirt.resources.events import event_cb

eventLoopThread = None

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

config_name = os.getenv('FLASK_CONFIGURATION', 'development')
app = create_app(config_name)

socketio = SocketIO(
        app=app,
        async_mode=async_mode)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.teardown_appcontext
def teardown_conn(exception):
    conn = getattr(g, 'libvirt_conn', None)
    if conn is not None:
        conn.disconnect()


def main():
    app.logger.info(config_name)

    with app.app_context():
        from pyvirt.utils.libvirt import get_virtconn
        from pyvirt.resources.domain import DomainList, Domain
        conn = get_virtconn()
        conn.register_event_cb(
            cb=lambda *args: event_cb(socketio, *args)
        )

        api = Api(app)
        api.add_resource(DomainList, '/api/domain')
        api.add_resource(Domain, '/api/domain/<string:uuid>')

        socketio.run(app, port=5555, use_reloader=False, debug=True)


if __name__ == '__main__':
    main()
