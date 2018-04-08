# coding=utf-8
import celery
import time
from flask_socketio import SocketIO


@celery.task()
def task(url):
    local_socketio = SocketIO(message_queue=url)
    local_socketio.emit('my response', {'data': 'background task starting ...'}, namespace='/libvirt')
    time.sleep(10)
    local_socketio.emit('my response', {'data': 'background task complete!'}, namespace='/libvirt')