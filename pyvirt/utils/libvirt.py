import libvirt
from flask import g
from flask import current_app as app


def get_virtconn():
    """Opens a new libvirt connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'libvirt_conn'):
        uri = app.config['XEN_URI']
        app.logger.info('Opening libvirt connection: {}'.format(uri))
        g.libvirt_conn = libvirt.openReadOnly(uri)

    return g.libvirt_conn