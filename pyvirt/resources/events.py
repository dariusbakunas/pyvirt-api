# coding=utf-8
from flask import current_app


def dom_event_to_string(event):
    domEventStrings = (
        "Defined",
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
        ("Added", "Updated"),
        ("Removed", ),
        ("Booted", "Migrated", "Restored", "Snapshot", "Wakeup"),
        ("Paused", "Migrated", "IOError", "Watchdog", "Restored", "Snapshot", "API error"),
        ("Unpaused", "Migrated", "Snapshot"),
        ("Shutdown", "Destroyed", "Crashed", "Migrated", "Saved", "Failed", "Snapshot"),
        ("Finished", "On guest request", "On host request"),
        ("Memory", "Disk"),
        ("Panicked", ),
    )
    return domEventStrings[event][detail]


def event_cb(socketio, conn, dom, event, detail, opaque):
    event_str = dom_event_to_string(event)
    current_app.logger.info('emitting libvirt event: {}', event_str)
    socketio.emit('libvirt_event', {
        'event': dom_event_to_string(event),
        'detail': dom_detail_to_string(event, detail),
        'uuid': dom.UUIDString(),
    }, namespace='/libvirt')
