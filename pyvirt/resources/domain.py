# coding=utf-8
import sys
from flask import jsonify
from flask_restful import Resource
from pyvirt.utils.libvirt import get_virtconn
from werkzeug.local import LocalProxy
from flask import current_app as app


class DomainList(Resource):
    @classmethod
    def set_libvirt_conn(cls, conn):
        cls.conn = conn
        return cls

    def get(self):
        try:
            virt_domains = self.conn.listAllDomains()
            response = [{
                "id": d.ID(),
                "name": d.name(),
                "uuid": d.UUIDString(),
                "isActive": d.isActive()
            } for d in virt_domains]
            return jsonify(response)
        except Exception as e:
            app.logger.error('failed to open libvirt connection')
            sys.exit(1)

    def post(self):
        pass


class Domain(Resource):
    def get(self, uuid):
        conn = LocalProxy(get_virtconn)
        domain = conn.lookupByUUIDString(uuid)
        info = domain.info()
        response = {
            'state': info[0],
            'maxMem': info[1],
            'memory': info[2],
            'nvVirtCpu': info[3],
            'cpuTime': info[4],
        }

        return jsonify(response)
