# coding=utf-8
import os
import time
from celery import Celery
from flask_socketio import SocketIO
from celery.utils.log import get_task_logger

from .events import event_cb
from .libvirt import LibvirtEventConnector

logger = get_task_logger(__name__)

env = os.environ
CELERY_BROKER_URL=env.get('CELERY_BROKER_URL', 'redis://redis:6379/0'),

celery = Celery('bg_tasks', broker=CELERY_BROKER_URL)


@celery.task(name='libvirt.event.loop')
def task(iomq_url, xen_url):
    conn = LibvirtEventConnector()
    conn.start_native_loop()
    conn.connect(xen_url)

    local_socketio = SocketIO(message_queue=iomq_url)
    conn.register_event_cb(
        cb=lambda *args: event_cb(local_socketio, *args)
    )

    while True:
        time.sleep(1)
