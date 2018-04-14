# coding=utf-8
import sys
from flask import jsonify
from flask_restful import Resource
from flask import current_app as app
from pyvirt.utils.libvirt import get_virtconn


class DomainList(Resource):
    def get(self):
        with app.app_context():
            try:
                conn = get_virtconn()
                virt_domains = conn.listAllDomains()
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
