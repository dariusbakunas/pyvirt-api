# coding=utf-8
from marshmallow import Schema, fields


class Domain(object):
    def __init__(self, id, uuid, name, is_active):
        self.name = name
        self.id = id
        self.uuid = uuid
        self.isActive = is_active

    def __repr__(self):
        return '<Domain(name={self.name!r}>'.format(self=self)


class DomainSchema(Schema):
    id = fields.Int()
    uuid = fields.Str()
    name = fields.Str()
    isActive = fields.Bool()