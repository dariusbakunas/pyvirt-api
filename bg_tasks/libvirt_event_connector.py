# coding=utf-8
import libvirt
import threading
import sys
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

eventLoopThread = None


class LibvirtEventConnector:
    def __init__(self):
        self.cb = None
        self.conn = None

    def _native_loop(self):
        while True:
            libvirt.virEventRunDefaultImpl()

    def _close_conn_cb(self, conn, reason, opaque):
        reasonStrings = (
            "Error", "End-of-file", "Keepalive", "Client",
        )
        logger.info("closing libvirt connection: %s: %s" % (conn.getURI(), reasonStrings[reason]))

    def start_native_loop(self):
        global eventLoopThread
        libvirt.virEventRegisterDefaultImpl()
        eventLoopThread = threading.Thread(target=self._native_loop, name="libvirtEventLoop")
        eventLoopThread.setDaemon(True)
        eventLoopThread.start()

    def connect(self, uri):
        logger.info('connecting to {}'.format(uri))
        self.conn = libvirt.openReadOnly(uri)
        self.conn.registerCloseCallback(self._close_conn_cb, None)
        self.conn.setKeepAlive(5, 3)

        if self.conn is None:
            logger.error('failed to open connection to the hypervisor')
            sys.exit(1)

        logger.info('connected to {}'.format(uri))

    def register_event_cb(self, cb):
        if self.cb is not None:
            self.conn.domainEventDeregister(self.cb)

        self.cb = cb
        self.conn.domainEventRegister(cb, None)

    def disconnect(self):
        if self.conn is not None:
            logger.info("Closing " + self.conn.getURI())
            if self.cb is not None:
                self.conn.domainEventDeregister(self.cb)
            self.conn.unregisterCloseCallback()
            self.conn.close()
