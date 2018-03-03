# coding=utf-8
import libvirt
import sys
from flask import g
from flask import current_app as app


def get_virtconn():
    conn = getattr(g, '_virtconn', None)
    if conn is None:
        conn = libvirt.openReadOnly(app.config['XEN_URI'])
        if conn is None:
            print('Failed to open connection to the hypervisor')
            sys.exit(1)
    return conn

@app.teardown_appcontext
def teardown_virtconn(exception):
    conn = getattr(g, '_virtconn', None)
    if conn is not None:
        conn.close()
