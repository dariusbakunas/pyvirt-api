# coding=utf-8
import sys
from flask import jsonify
from flask_restful import Resource
from pyvirt.model.domain import Domain as DomainModel, DomainSchema
from pyvirt.utils.virtconn import get_virtconn
from werkzeug.local import LocalProxy


class DomainList(Resource):
    def get(self):
        conn = LocalProxy(get_virtconn)
        try:
            schema = DomainSchema(many=True)
            virt_domains = conn.listAllDomains()
            domains = schema.dump(
                [
                    DomainModel(
                        id=d.ID,
                        name=d.name,
                        uuid=d.UUIDString,
                        is_active=d.isActive
                    ) for d in virt_domains
                ]
            )

            return jsonify(domains.data)
        except:
            print('Failed to find the main domain')
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
