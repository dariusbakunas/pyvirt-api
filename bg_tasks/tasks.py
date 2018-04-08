# coding=utf-8
import os
import time
from celery import Celery
from flask_socketio import SocketIO

env = os.environ
CELERY_BROKER_URL=env.get('CELERY_BROKER_URL', 'redis://localhost:6379'),

celery = Celery('bg_tasks', broker=CELERY_BROKER_URL)


@celery.task(name='libvirt.event.loop')
def task(url):
    local_socketio = SocketIO(message_queue=url)
    local_socketio.emit('libvirt-event', {'data': 'background task starting ...'}, namespace='/libvirt')
    time.sleep(10)
    local_socketio.emit('libvirt-event', {'data': 'background task complete!'}, namespace='/libvirt')
