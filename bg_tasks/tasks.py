# coding=utf-8
import os
from celery import Celery
from flask_socketio import SocketIO
from celery.utils.log import get_task_logger

from .events import event_cb
from .libvirt import LibvirtEventConnector

logger = get_task_logger(__name__)

env = os.environ
CELERY_BROKER_URL=env.get('CELERY_BROKER_URL', 'redis://redis:6379/0'),

celery = Celery('bg_tasks', broker=CELERY_BROKER_URL)
conn = None


@celery.task(name='libvirt.event.loop.start')
def start_libvirt_loop_task(iomq_url, xen_url):
    global conn
    conn = LibvirtEventConnector()
    conn.start_native_loop()
    conn.connect(xen_url)

    local_socketio = SocketIO(message_queue=iomq_url)
    conn.register_event_cb(
        cb=lambda *args: event_cb(local_socketio, *args)
    )
