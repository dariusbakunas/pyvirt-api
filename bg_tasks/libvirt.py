# coding=utf-8
import libvirt
import threading
import sys

eventLoopThread = None


class LibvirtEventConnector:
    def __init__(self, logger):
        self.cb = None
        self.conn = None
        self.logger = logger

    def _aio_loop(self, loop):
        import asyncio
        import libvirtaio
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def _native_loop(self):
        while True:
            libvirt.virEventRunDefaultImpl()

    def _close_conn_cb(self, conn, reason, opaque):
        reasonStrings = (
            "Error", "End-of-file", "Keepalive", "Client",
        )
        self.logger.info("closing libvirt connection: %s: %s" % (conn.getURI(), reasonStrings[reason]))

    def start_aio_loop(self):
        import asyncio
        import libvirtaio
        global eventLoopThread
        loop = asyncio.new_event_loop()
        libvirtaio.virEventRegisterAsyncIOImpl(loop=loop)
        eventLoopThread = threading.Thread(
            target=self._aio_loop,
            args=(loop,),
            name="libvirtEventLoop")
        eventLoopThread.setDaemon(True)
        eventLoopThread.start()

    def start_native_loop(self):
        global eventLoopThread
        libvirt.virEventRegisterDefaultImpl()
        eventLoopThread = threading.Thread(target=self._native_loop, name="libvirtEventLoop")
        eventLoopThread.setDaemon(True)
        eventLoopThread.start()

    def connect(self, uri):
        self.logger.info('connecting to {}'.format(uri))
        self.conn = libvirt.openReadOnly(uri)
        self.conn.registerCloseCallback(self._close_conn_cb, None)
        self.conn.setKeepAlive(5, 3)

        if self.conn is None:
            self.logger.error('failed to open connection to the hypervisor')
            sys.exit(1)

    def register_event_cb(self, cb):
        if self.cb is not None:
            self.conn.domainEventDeregister(self.cb)

        self.cb = cb
        self.conn.domainEventRegister(cb, None)

    def disconnect(self):
        if self.conn is not None:
            self.logger.info("Closing " + self.conn.getURI())
            if self.cb is not None:
                self.conn.domainEventDeregister(self.cb)
            self.conn.unregisterCloseCallback()
            self.conn.close()
