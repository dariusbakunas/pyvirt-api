# coding=utf-8
import sys
import libvirt
from flask import jsonify
from flask_restful import Resource
from flask import current_app as app


class DomainList(Resource):
    def get(self):
        with app.app_context():
            conn = None

            try:
                conn = libvirt.openReadOnly(app.config['XEN_URI'])
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
            finally:
                if conn:
                    conn.close()
