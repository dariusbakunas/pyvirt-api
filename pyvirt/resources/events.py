# coding=utf-8
from flask_socketio import Namespace, emit
from flask import request

def dem_event_to_string(event):
    domEventStrings = ( "Defined",
                     "Undefined",
                     "Started",
                     "Suspended",
                     "Resumed",
                     "Stopped",
                     "Shutdown",
                     "PMSuspended",
                     "Crashed",
    )
    return domEventStrings[event]


def dom_detail_to_string(event, detail):
    domEventStrings = (
        ( "Added", "Updated" ),
        ( "Removed", ),
        ( "Booted", "Migrated", "Restored", "Snapshot", "Wakeup" ),
        ( "Paused", "Migrated", "IOError", "Watchdog", "Restored", "Snapshot", "API error" ),
        ( "Unpaused", "Migrated", "Snapshot" ),
        ( "Shutdown", "Destroyed", "Crashed", "Migrated", "Saved", "Failed", "Snapshot"),
        ( "Finished", "On guest request", "On host request"),
        ( "Memory", "Disk" ),
        ( "Panicked", ),
        )
    return domEventStrings[event][detail]

def event_cb(socketio, conn, dom, event, detail, opaque):
    socketio.emit('libvirt_event', {'event': dem_event_to_string(event)},
                  namespace='/libvirt')
    # print("myDomainEventCallback1 EVENT: Domain %s(%s) %s %s" % (
    # dom.name(), dom.ID(),
    # domEventToString(event),
    # domDetailToString(event, detail)))