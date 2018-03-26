# coding=utf-8
import libvirt
import threading
import sys
import libvirtaio
import asyncio
from flask import g
from flask import current_app as app


class LibvirtConnector:
    def __init__(self):
        self.cb = None

    def _aio_loop(self, loop):
        import asyncio
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def _close_conn_cb(self, conn, reason, opaque):
        reasonStrings = (
            "Error", "End-of-file", "Keepalive", "Client",
        )
        print("myConnectionCloseCallback: %s: %s" % (
        conn.getURI(), reasonStrings[reason]))

    def start_event_loop(self):
        global eventLoopThread
        loop = asyncio.new_event_loop()
        libvirtaio.virEventRegisterAsyncIOImpl(loop=loop)
        eventLoopThread = threading.Thread(
            target=self._aio_loop,
            args=(loop,),
            name="libvirtEventLoop")
        eventLoopThread.setDaemon(True)
        eventLoopThread.start()

    def connect(self, uri):
        self.conn = libvirt.openReadOnly(uri)
        self.conn.registerCloseCallback(self._close_conn_cb, None)
        self.conn.setKeepAlive(5, 3)

        if self.conn is None:
            print('Failed to open connection to the hypervisor')
            sys.exit(1)

    def register_event_cb(self, cb):
        if self.cb is not None:
            self.conn.domainEventDeregister(self.cb)

        self.cb = cb
        self.conn.domainEventRegister(cb, None)

    def disconnect(self):
        if self.conn is not None:
            print("Closing " + self.conn.getURI())
            if self.cb is not None:
                self.conn.domainEventDeregister(self.cb)
            self.conn.unregisterCloseCallback()
            self.conn.close()


def get_virtconn():
    """Opens a new libvirt connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'libvirt_conn'):
        g.libvirt_conn = LibvirtConnector()
        g.libvirt_conn.start_event_loop()
        g.libvirt_conn.connect(app.config['XEN_URI'])

    return g.libvirt_conn