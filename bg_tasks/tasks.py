# coding=utf-8
import os
import time
from celery import Celery
from flask_socketio import SocketIO

env = os.environ
CELERY_BROKER_URL=env.get('CELERY_BROKER_URL', 'redis://redis:6379/0'),
CELERY_RESULT_BACKEND=env.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

celery = Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)


@celery.task(name='libvirt.event.loop')
def task(url):
    local_socketio = SocketIO(message_queue=url)
    local_socketio.emit('libvirt-event', {'data': 'background task starting ...'}, namespace='/libvirt')
    time.sleep(10)
    local_socketio.emit('libvirt-event', {'data': 'background task complete!'}, namespace='/libvirt')
