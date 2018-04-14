# coding=utf-8
import time
import os
import logging
from flask_socketio import SocketIO
from bg_tasks.events import event_cb
from bg_tasks.libvirt_event_connector import LibvirtEventConnector
from instance import config

logger = logging.getLogger(__name__)
env = os.environ

logging.basicConfig(level=env.get('LOG_LEVEL', 'INFO'))


if not config.XEN_URI:
    raise ValueError('XEN_URI must be specified')

if not config.REDIS_URL:
    raise ValueError('REDIS_URL must be specified')


def main():
    logger.info('Starting background worker..')
    sio = SocketIO(message_queue=config.REDIS_URL)
    conn = LibvirtEventConnector()
    conn.start_native_loop()
    conn.connect(config.XEN_URI)
    conn.register_event_cb(
        cb=lambda *args: event_cb(sio, *args)
    )

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
